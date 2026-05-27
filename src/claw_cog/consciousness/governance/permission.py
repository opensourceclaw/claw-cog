"""PermissionController — operation permission management."""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk level of an operation."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PermissionDecision(Enum):
    """Permission decision for an operation."""

    ALLOW = "allow"
    DENY = "deny"
    WARN = "warn"


class Role(Enum):
    """Access roles for permission control."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class PermissionResult:
    """Result of a permission check.

    Attributes:
        decision: allow / deny / warn.
        reason: Human-readable explanation.
        risk_level: Assessed risk level.
        role: The role that was checked.
    """

    decision: PermissionDecision = PermissionDecision.ALLOW
    reason: str = ""
    risk_level: RiskLevel = RiskLevel.LOW
    role: Role = Role.ASSISTANT


class PermissionController:
    """Controls operation permissions based on risk level and role.

    Implements role-based access control with configurable
    permission matrices for different risk levels.

    Example:
        >>> pc = PermissionController()
        >>> pc.set_role_permission(
        ...     Role.ASSISTANT, RiskLevel.HIGH, PermissionDecision.DENY
        ... )
        >>> result = pc.check("rm file", Role.ASSISTANT)
        >>> print(result.decision, result.reason)
    """

    # Default permission matrix: role -> risk -> decision
    DEFAULT_MATRIX: Dict[Role, Dict[RiskLevel, PermissionDecision]] = {
        Role.USER: {
            RiskLevel.LOW: PermissionDecision.ALLOW,
            RiskLevel.MEDIUM: PermissionDecision.WARN,
            RiskLevel.HIGH: PermissionDecision.DENY,
            RiskLevel.CRITICAL: PermissionDecision.DENY,
        },
        Role.ASSISTANT: {
            RiskLevel.LOW: PermissionDecision.ALLOW,
            RiskLevel.MEDIUM: PermissionDecision.ALLOW,
            RiskLevel.HIGH: PermissionDecision.WARN,
            RiskLevel.CRITICAL: PermissionDecision.DENY,
        },
        Role.SYSTEM: {
            RiskLevel.LOW: PermissionDecision.ALLOW,
            RiskLevel.MEDIUM: PermissionDecision.ALLOW,
            RiskLevel.HIGH: PermissionDecision.ALLOW,
            RiskLevel.CRITICAL: PermissionDecision.WARN,
        },
    }

    def __init__(self):
        self._matrix: Dict = {}
        for role, risks in self.DEFAULT_MATRIX.items():
            self._matrix[role] = dict(risks)

    def set_role_permission(
        self, role: Role, risk_level: RiskLevel, decision: PermissionDecision
    ) -> None:
        """Set permission for a role at a risk level.

        Args:
            role: The Role to configure.
            risk_level: The RiskLevel.
            decision: The PermissionDecision.
        """
        if role not in self._matrix:
            self._matrix[role] = {}
        self._matrix[role][risk_level] = decision

    def get_role_permission(
        self, role: Role, risk_level: RiskLevel
    ) -> PermissionDecision:
        """Get the current permission for a role at a risk level."""
        return self._matrix.get(role, {}).get(
            risk_level, PermissionDecision.DENY
        )

    def classify_risk(self, operation: str) -> RiskLevel:
        """Classify the risk level of an operation.

        Args:
            operation: The operation name/description.

        Returns:
            RiskLevel enumeration value.
        """
        op_lower = operation.lower()

        # Critical patterns
        critical = ["delete", "remove", "truncate", "drop", "format"]
        for p in critical:
            if p in op_lower:
                return RiskLevel.CRITICAL

        # High risk patterns
        high = ["write", "modify", "change", "config", "deploy", "execute"]
        for p in high:
            if p in op_lower:
                return RiskLevel.HIGH

        # Medium risk
        medium = ["read", "open", "query", "search", "fetch", "get"]
        for p in medium:
            if p in op_lower:
                return RiskLevel.MEDIUM

        return RiskLevel.LOW

    def check(
        self, operation: str, role: Role = Role.ASSISTANT,
        context: Optional[Dict] = None,
    ) -> PermissionResult:
        """Check if an operation is permitted.

        Args:
            operation: The operation to check.
            role: The requesting role.
            context: Optional context.

        Returns:
            PermissionResult with decision and reason.
        """
        risk = self.classify_risk(operation)
        decision = self.get_role_permission(role, risk)

        reason = (
            f"Role '{role.value}' is {decision.value}ed for "
            f"'{risk.value}' risk operation: {operation}"
        )

        return PermissionResult(
            decision=decision,
            reason=reason,
            risk_level=risk,
            role=role,
        )
