"""SafetyBoundary — defines allowed/disallowed operation domains."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set
import logging

logger = logging.getLogger(__name__)


class BoundaryDecision(Enum):
    """Result of a safety boundary check."""

    ALLOWED = "allowed"
    DENIED = "denied"
    RESTRICTED = "restricted"


@dataclass
class BoundaryRule:
    """A single boundary rule.

    Attributes:
        name: Human-readable rule name.
        description: What this rule checks.
        domain: Operation domain (e.g. "file_system", "network").
        allowed_operations: Operation names that are explicitly allowed.
        denied_operations: Operation names that are explicitly denied.
        restricted_patterns: Content patterns that trigger restriction.
    """

    name: str
    description: str = ""
    domain: str = "general"
    allowed_operations: Set[str] = field(default_factory=set)
    denied_operations: Set[str] = field(default_factory=set)
    restricted_patterns: List[str] = field(default_factory=list)


class SafetyBoundary:
    """Defines and enforces allowed/disallowed operation domains.

    Configurable rules that check whether an action falls within
    safe operational bounds.

    Example:
        >>> boundary = SafetyBoundary()
        >>> boundary.add_rule(BoundaryRule(
        ...     name="no_file_delete", domain="file_system",
        ...     denied_operations={"delete", "rm", "rmdir"},
        ... ))
        >>> result = boundary.check("delete", domain="file_system")
    """

    # Built-in safe defaults
    DEFAULT_RULES: List[BoundaryRule] = []

    def __init__(self):
        self._rules: Dict[str, BoundaryRule] = {}
        self._init_defaults()

    def _init_defaults(self) -> None:
        """Initialize default safety rules."""
        defaults = [
            BoundaryRule(
                name="no_file_system_delete",
                description="Prevent accidental file deletion",
                domain="file_system",
                denied_operations={"rm", "rmdir", "delete", "unlink", "rmtree"},
            ),
            BoundaryRule(
                name="no_system_modification",
                description="Prevent system-level modifications",
                domain="system",
                denied_operations={"chmod", "chown", "mount", "mkfs", "shutdown", "reboot"},
            ),
            BoundaryRule(
                name="restrict_network_bind",
                description="Restrict network port binding",
                domain="network",
                restricted_patterns=["bind", "listen"],
            ),
        ]
        for rule in defaults:
            self._rules[rule.name] = rule

    def add_rule(self, rule: BoundaryRule) -> None:
        """Add a safety boundary rule.

        Args:
            rule: The BoundaryRule to add.

        Raises:
            ValueError: If rule with same name exists.
        """
        if rule.name in self._rules:
            raise ValueError(f"Rule '{rule.name}' already exists")
        self._rules[rule.name] = rule

    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name."""
        if name in self._rules:
            del self._rules[name]
            return True
        return False

    def check(
        self,
        operation: str,
        domain: str = "general",
        context: Optional[Dict] = None,
    ) -> tuple:
        """Check if an operation is within safe bounds.

        Args:
            operation: The operation name/description to check.
            domain: The operation domain.
            context: Optional context for pattern matching.

        Returns:
            Tuple of (BoundaryDecision, reason_string).
        """
        for rule in self._rules.values():
            if rule.domain != domain:
                continue

            op_lower = operation.lower()

            # Check denied operations
            for denied in rule.denied_operations:
                if denied.lower() in op_lower:
                    return BoundaryDecision.DENIED, (
                        f"Operation '{operation}' denied by rule '{rule.name}': {rule.description}"
                    )

            # Check restricted patterns
            for pattern in rule.restricted_patterns:
                if pattern.lower() in op_lower:
                    return BoundaryDecision.RESTRICTED, (
                        f"Operation '{operation}' restricted by rule "
                        f"'{rule.name}': matches pattern '{pattern}'"
                    )

            # If there's an explicit allow list, check it
            if rule.allowed_operations:
                allowed = any(a.lower() in op_lower for a in rule.allowed_operations)
                if not allowed:
                    return BoundaryDecision.DENIED, (
                        f"Operation '{operation}' not in allowed list for "
                        f"domain '{domain}' (rule: {rule.name})"
                    )

        return BoundaryDecision.ALLOWED, f"Operation '{operation}' allowed"

    def get_rules(self) -> List[BoundaryRule]:
        """Get all registered rules."""
        return list(self._rules.values())
