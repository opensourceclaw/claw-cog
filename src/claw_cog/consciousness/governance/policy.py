"""PolicyEnforcer — governance pipeline orchestrator."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional
import logging

from .boundary import SafetyBoundary, BoundaryDecision
from .permission import (
    PermissionController, PermissionDecision, Role,
)
from .audit import AuditLogger
from .guardrails.input_filter import InputFilter
from .guardrails.output_filter import OutputFilter
from .guardrails.behavior_constraint import BehaviorConstraint

logger = logging.getLogger(__name__)


class PolicyDecision(Enum):
    """Overall policy decision."""

    ALLOWED = "allowed"
    DENIED = "denied"
    RESTRICTED = "restricted"


@dataclass
class PolicyResult:
    """Result of a full governance policy evaluation.

    Attributes:
        allowed: Whether the action is permitted.
        decision: Overall decision (allowed/denied/restricted).
        explanation: Human-readable explanation.
        boundary_decision: Safety boundary check result.
        permission_decision: Permission check result.
        details: Additional context details.
    """

    allowed: bool = True
    decision: PolicyDecision = PolicyDecision.ALLOWED
    explanation: str = ""
    boundary_decision: Optional[str] = None
    permission_decision: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


class PolicyEnforcer:
    """Executes governance policies across the pipeline.

    Composes SafetyBoundary, PermissionController, and guardrails
    into a single governance check. Logs all decisions via AuditLogger.

    Pipeline: input_filter -> boundary_check -> permission_check -> output_filter

    Example:
        >>> enforcer = PolicyEnforcer()
        >>> result = enforcer.evaluate_input("delete production database")
        >>> result = enforcer.evaluate_action("write", Role.ASSISTANT)
        >>> result = enforcer.evaluate_output("sensitive data here")
    """

    def __init__(
        self,
        boundary: Optional[SafetyBoundary] = None,
        permission: Optional[PermissionController] = None,
        audit: Optional[AuditLogger] = None,
    ):
        self.boundary = boundary or SafetyBoundary()
        self.permission = permission or PermissionController()
        self.audit = audit or AuditLogger()
        self.input_filter = InputFilter()
        self.output_filter = OutputFilter()
        self.behavior_constraint = BehaviorConstraint()

    def evaluate_input(
        self, content: str, role: Role = Role.ASSISTANT,
    ) -> PolicyResult:
        """Evaluate input content through governance.

        Pipeline: input_filter -> boundary_check -> permission_check

        Args:
            content: The input content to evaluate.
            role: The requesting role.

        Returns:
            PolicyResult with evaluation details.
        """
        details: Dict[str, Any] = {}

        # Step 1: Input filtering
        is_safe, filtered, reason = self.input_filter.filter(content)
        if not is_safe:
            self.audit.log("InputFilter", content[:50], "denied", reason)
            return PolicyResult(
                allowed=False, decision=PolicyDecision.DENIED,
                explanation=f"Input rejected: {reason}",
                details={"filtered_content": filtered},
            )

        # Step 2: Safety boundary check
        b_decision, b_reason = self.boundary.check(content)
        details["boundary"] = {"decision": b_decision.value, "reason": b_reason}
        if b_decision == BoundaryDecision.DENIED:
            self.audit.log("SafetyBoundary", content[:50], "denied", b_reason,
                          details)
            return PolicyResult(
                allowed=False, decision=PolicyDecision.DENIED,
                explanation=b_reason,
                boundary_decision=b_decision.value, details=details,
            )

        # Step 3: Permission check
        p_result = self.permission.check(content, role)
        details["permission"] = {
            "decision": p_result.decision.value,
            "risk": p_result.risk_level.value,
        }
        if p_result.decision == PermissionDecision.DENY:
            self.audit.log("PermissionController", content[:50], "denied",
                          p_result.reason, details)
            return PolicyResult(
                allowed=False, decision=PolicyDecision.DENIED,
                explanation=p_result.reason,
                permission_decision=p_result.decision.value, details=details,
            )

        # Final decision
        if b_decision == BoundaryDecision.RESTRICTED or \
           p_result.decision == PermissionDecision.WARN:
            self.audit.log("PolicyEnforcer", content[:50], "restricted",
                          b_reason, details)
            return PolicyResult(
                allowed=True, decision=PolicyDecision.RESTRICTED,
                explanation=f"Restricted: {b_reason}\n{p_result.reason}",
                boundary_decision=b_decision.value,
                permission_decision=p_result.decision.value,
                details=details,
            )

        self.audit.log("PolicyEnforcer", content[:50], "allowed", "", details)
        return PolicyResult(
            allowed=True, decision=PolicyDecision.ALLOWED,
            explanation="Input passed all governance checks",
            boundary_decision=b_decision.value,
            permission_decision=p_result.decision.value,
            details=details,
        )

    def evaluate_action(
        self, operation: str, role: Role = Role.ASSISTANT,
        domain: str = "general",
    ) -> PolicyResult:
        """Evaluate an action/operation through governance.

        Args:
            operation: The operation to evaluate.
            role: The requesting role.
            domain: The operation domain.

        Returns:
            PolicyResult.
        """
        details: Dict[str, Any] = {}

        # Behavior constraint check
        allowed, constraint_reason = self.behavior_constraint.check(operation)
        if not allowed:
            self.audit.log("BehaviorConstraint", operation, "denied", constraint_reason)
            return PolicyResult(
                allowed=False, decision=PolicyDecision.DENIED,
                explanation=constraint_reason, details=details,
            )

        # Safety boundary
        b_decision, b_reason = self.boundary.check(operation, domain)
        details["boundary"] = {"decision": b_decision.value, "reason": b_reason}
        if b_decision == BoundaryDecision.DENIED:
            self.audit.log("SafetyBoundary", operation, "denied", b_reason, details)
            return PolicyResult(
                allowed=False, decision=PolicyDecision.DENIED,
                explanation=b_reason, boundary_decision=b_decision.value,
                details=details,
            )

        # Permission
        p_result = self.permission.check(operation, role)
        details["permission"] = {"decision": p_result.decision.value}
        if p_result.decision == PermissionDecision.DENY:
            self.audit.log("PermissionController", operation, "denied", p_result.reason)
            return PolicyResult(
                allowed=False, decision=PolicyDecision.DENIED,
                explanation=p_result.reason,
                permission_decision=p_result.decision.value,
                details=details,
            )

        self.audit.log("PolicyEnforcer", operation, "allowed", "", details)
        return PolicyResult(
            allowed=True, decision=PolicyDecision.ALLOWED,
            explanation="Action allowed",
            boundary_decision=b_decision.value,
            permission_decision=p_result.decision.value,
            details=details,
        )

    def evaluate_output(
        self, content: str,
    ) -> PolicyResult:
        """Evaluate output content through governance.

        Args:
            content: The output content to evaluate.

        Returns:
            PolicyResult.
        """
        is_safe, filtered, reason = self.output_filter.filter(content)
        if not is_safe:
            self.audit.log("OutputFilter", content[:50], "denied", reason)
            return PolicyResult(
                allowed=False, decision=PolicyDecision.DENIED,
                explanation=f"Output rejected: {reason}",
                details={"filtered_content": filtered},
            )

        self.audit.log("OutputFilter", content[:50], "allowed", "")
        return PolicyResult(
            allowed=True, decision=PolicyDecision.ALLOWED,
            explanation="Output passed governance",
        )

    def get_audit_summary(self) -> Dict[str, Any]:
        """Get governance audit summary."""
        return self.audit.get_summary()

    def reset(self) -> None:
        """Reset all governance components."""
        self.audit.clear()
