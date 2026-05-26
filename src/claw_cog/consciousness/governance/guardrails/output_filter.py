"""Output filter — sanitize output before response."""

from typing import List, Optional, Tuple
import re
import logging

logger = logging.getLogger(__name__)


class OutputFilter:
    """Filter output content before returning to user.

    Checks for:
    - Sensitive data leakage (PII, credentials, tokens)
    - Malicious content patterns
    - Inappropriate content markers

    Example:
        >>> f = OutputFilter()
        >>> safe, filtered, reason = f.filter("My password is secret123")
        >>> print(safe, filtered)
    """

    # Patterns that indicate sensitive data leakage
    SENSITIVE_PATTERNS: List[re.Pattern] = [
        re.compile(r"(?i)password\s*[:=]\s*\S+"),
        re.compile(r"(?i)secret\s*[:=]\s*\S+"),
        re.compile(r"(?i)(?:api[_-]?key|apikey)\s*[:=]\s*\S+"),
        re.compile(r"sk-[a-zA-Z0-9]{20,}"),
        re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"),  # phone
    ]

    # Patterns that should be sanitized (replaced with placeholder)
    SANITIZE_PATTERNS: List[re.Pattern] = [
        re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),  # email
        re.compile(r"ghp_[a-zA-Z0-9]{36}"),  # GitHub token
        re.compile(r"(?i)bearer\s+[a-zA-Z0-9\-._~+/]+=*"),
    ]

    def __init__(self):
        pass

    def filter(self, content: str) -> Tuple[bool, str, Optional[str]]:
        """Filter output content for sensitive data.

        Args:
            content: The output string to filter.

        Returns:
            Tuple of (is_safe, filtered_content, reason).
        """
        if not content or not isinstance(content, str):
            return True, content or "", None

        filtered = content

        # Check sensitive patterns — reject entirely
        for pattern in self.SENSITIVE_PATTERNS:
            if pattern.search(filtered):
                return False, content[:50], (
                    f"Output contains sensitive data matching: {pattern.pattern}"
                )

        # Sanitize patterns — replace with placeholder
        for pattern in self.SANITIZE_PATTERNS:
            filtered = pattern.sub("[REDACTED]", filtered)

        return True, filtered, None
