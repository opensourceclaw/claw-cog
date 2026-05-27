"""Behavior constraint — constrain agent behavior patterns."""

from typing import List, Optional, Set, Tuple
import re
import logging

logger = logging.getLogger(__name__)


class BehaviorConstraint:
    """Enforces constraints on agent behavior patterns.

    Defines rules that limit what operations an agent can perform,
    based on configurable deny lists and pattern matching.

    Example:
        >>> bc = BehaviorConstraint()
        >>> bc.deny_operation("sudo_command", "rm -rf /")
        >>> allowed, reason = bc.check("run rm -rf /")
        >>> print(allowed, reason)
    """

    # Built-in constraints
    DEFAULT_DENIED_OPERATIONS: Set[str] = {
        "sudo_command",
        "system_call",
        "shell_exec",
        "raw_sql_execution",
        "unrestricted_file_write",
    }

    DEFAULT_DENIED_PATTERNS: List[re.Pattern] = [
        re.compile(r"(?i)rm\s+-rf\s+/"),
        re.compile(r"(?i)dd\s+if="),
        re.compile(r"(?i)>/dev/[a-z]*da"),
        re.compile(r"(?i)fork\s+bomb"),
    ]

    def __init__(self):
        self._denied_operations: Set[str] = set(self.DEFAULT_DENIED_OPERATIONS)
        self._denied_patterns: List[re.Pattern] = list(
            self.DEFAULT_DENIED_PATTERNS
        )

    def deny_operation(self, operation_type: str, pattern: Optional[str] = None) -> None:
        """Add an operation type to the deny list.

        Args:
            operation_type: Operation type to deny.
            pattern: Optional regex pattern to deny.
        """
        self._denied_operations.add(operation_type)
        if pattern:
            self._denied_patterns.append(re.compile(pattern))

    def allow_operation(self, operation_type: str) -> bool:
        """Remove an operation type from the deny list.

        Args:
            operation_type: Operation type to allow.

        Returns:
            True if removed.
        """
        if operation_type in self._denied_operations:
            self._denied_operations.remove(operation_type)
            return True
        return False

    def check(
        self, operation: str, operation_type: Optional[str] = None
    ) -> Tuple[bool, Optional[str]]:
        """Check if an operation violates behavior constraints.

        Args:
            operation: The operation description/command.
            operation_type: Optional operation type for direct deny-list check.

        Returns:
            Tuple of (allowed: bool, reason: str|None).
        """
        # Check explicit deny list
        if operation_type and operation_type in self._denied_operations:
            return False, (
                f"Operation type '{operation_type}' is explicitly denied"
            )

        # Check denied patterns
        for pattern in self._denied_patterns:
            if pattern.search(operation):
                return False, (
                    f"Operation matches denied pattern: {pattern.pattern}"
                )

        return True, None

    def get_denied_operations(self) -> Set[str]:
        """Get the set of denied operation types."""
        return set(self._denied_operations)
