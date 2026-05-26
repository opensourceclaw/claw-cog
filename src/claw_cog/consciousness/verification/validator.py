"""Output validation for verification layer."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ValidationStatus(Enum):
    """Status of a single validation check."""

    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"


@dataclass
class ValidationResult:
    """Result of output validation.

    Attributes:
        status: Overall validation status.
        checks: List of individual check results as (rule_name, status, message).
        passed: Number of passed checks.
        failed: Number of failed checks.
        warned: Number of warning checks.
    """

    status: ValidationStatus = ValidationStatus.PASS
    checks: List = field(default_factory=list)
    passed: int = 0
    failed: int = 0
    warned: int = 0

    def add_check(self, rule_name: str, status: ValidationStatus, message: str = "") -> None:
        """Add a single check result.

        Args:
            rule_name: Name of the validation rule.
            status: Pass/Fail/Warn status.
            message: Optional descriptive message.
        """
        self.checks.append((rule_name, status, message))
        if status == ValidationStatus.PASS:
            self.passed += 1
        elif status == ValidationStatus.FAIL:
            self.failed += 1
        elif status == ValidationStatus.WARN:
            self.warned += 1

        # Update overall status
        if status == ValidationStatus.FAIL:
            self.status = ValidationStatus.FAIL
        elif status == ValidationStatus.WARN and self.status == ValidationStatus.PASS:
            self.status = ValidationStatus.WARN


class OutputValidator:
    """Validates output against a set of configurable rules.

    Rules are callables that take (output, context) and return
    (ValidationStatus, message). Rules can be added dynamically.

    Example:
        >>> validator = OutputValidator()
        >>> validator.add_rule("non_empty", lambda o, c: (
        ...     ValidationStatus.PASS if o else ValidationStatus.FAIL,
        ...     "Output is non-empty" if o else "Output is empty"
        ... ))
        >>> result = validator.validate("hello", {})
        >>> print(result.status)
    """

    def __init__(self):
        self._rules: Dict[str, Callable] = {}

    def add_rule(self, name: str, rule_func: Callable) -> None:
        """Add a validation rule.

        Args:
            name: Unique name for the rule.
            rule_func: Callable that takes (output, context) and returns
                       (ValidationStatus, str).

        Raises:
            ValueError: If a rule with the same name already exists.
        """
        if name in self._rules:
            raise ValueError(f"Rule '{name}' already exists")
        self._rules[name] = rule_func

    def remove_rule(self, name: str) -> bool:
        """Remove a validation rule by name.

        Args:
            name: Name of the rule to remove.

        Returns:
            True if the rule was removed, False if not found.
        """
        if name in self._rules:
            del self._rules[name]
            return True
        return False

    def validate(self, output: Any, context: Optional[Dict] = None) -> ValidationResult:
        """Validate output against all registered rules.

        Args:
            output: The output to validate.
            context: Optional context dict for rule evaluation.

        Returns:
            ValidationResult with overall status and per-check details.
        """
        if context is None:
            context = {}

        result = ValidationResult()

        if not self._rules:
            return result

        for rule_name, rule_func in self._rules.items():
            try:
                status, message = rule_func(output, context)
                result.add_check(rule_name, status, message)
            except Exception as e:
                logger.warning(f"Rule '{rule_name}' raised exception: {e}")
                result.add_check(
                    rule_name,
                    ValidationStatus.FAIL,
                    f"Rule execution error: {e}",
                )

        return result

    def validate_against(self, output: Any, expected: Any,
                         context: Optional[Dict] = None) -> ValidationResult:
        """Validate output against an expected value in addition to rules.

        Args:
            output: The output to validate.
            expected: The expected output value.
            context: Optional context dict.

        Returns:
            ValidationResult including an equality check.
        """
        if context is None:
            context = {}

        result = self.validate(output, context)
        eq_status = ValidationStatus.PASS if output == expected else ValidationStatus.FAIL
        result.add_check(
            "expected_match",
            eq_status,
            "Output matches expected value" if output == expected
            else f"Expected {expected!r} but got {output!r}",
        )
        return result

    def reset(self) -> None:
        """Remove all registered rules."""
        self._rules.clear()

    @property
    def rule_count(self) -> int:
        """Number of registered rules."""
        return len(self._rules)
