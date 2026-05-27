"""Input filter — sanitize input before processing."""

from typing import List, Optional, Tuple
import re
import logging

logger = logging.getLogger(__name__)


class InputFilter:
    """Filter input content before it enters the processing pipeline.

    Checks for:
    - Blacklisted patterns (injection, XSS, etc.)
    - Sensitive data patterns
    - Excessively long inputs

    Example:
        >>> f = InputFilter()
        >>> safe, filtered, reason = f.filter("DROP TABLE users;")
        >>> print(safe, reason)
    """

    # Patterns that indicate potentially dangerous input
    BLOCKED_PATTERNS: List[re.Pattern] = [
        re.compile(r"(?i)\bDROP\s+TABLE\b"),
        re.compile(r"(?i)\bDROP\s+DATABASE\b"),
        re.compile(r"(?i)\bTRUNCATE\s+TABLE\b"),
        re.compile(r"(?i)<script\b"),
        re.compile(r"(?i)\bDELETE\s+FROM\b"),
        re.compile(r"(?i)\bINSERT\s+INTO\b"),
        re.compile(r"(?i)\bUPDATE\s+.*\bSET\b"),
        re.compile(r"\$\{.+\}"),  # Template injection
        re.compile(r"\{\{.+\}\}"),  # Template injection
    ]

    # Patterns that should trigger a warning and strip
    WARN_PATTERNS: List[re.Pattern] = [
        re.compile(r"(?i)\bexec\("),
        re.compile(r"(?i)\beval\("),
        re.compile(r"(?i)\bsystem\("),
        re.compile(r"(?i)\bsubprocess\b"),
        re.compile(r"\|.*;"),  # Pipe to shell
    ]

    def __init__(self, max_input_length: int = 10000):
        """Initialize input filter.

        Args:
            max_input_length: Maximum allowed input length in chars.
        """
        self.max_input_length = max_input_length

    def filter(self, content: str) -> Tuple[bool, str, Optional[str]]:
        """Filter input content.

        Args:
            content: The input string to filter.

        Returns:
            Tuple of (is_safe: bool, filtered_content: str, reason: str|None).
        """
        if not content or not isinstance(content, str):
            return True, content or "", None

        # Length check
        if len(content) > self.max_input_length:
            truncated = content[: self.max_input_length]
            return (
                False,
                truncated,
                (f"Input exceeds max length ({len(content)} > {self.max_input_length})"),
            )

        # Blocked patterns
        for pattern in self.BLOCKED_PATTERNS:
            if pattern.search(content):
                return False, content[:50], (f"Input matches blocked pattern: {pattern.pattern}")

        # Warning patterns — sanitize but allow
        filtered = content
        for pattern in self.WARN_PATTERNS:
            if pattern.search(filtered):
                filtered = pattern.sub("[SANITIZED]", filtered)
                logger.debug(f"Sanitized pattern: {pattern.pattern}")

        return True, filtered, None
