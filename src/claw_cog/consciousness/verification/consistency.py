"""Consistency checking for verification layer."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConsistencyResult:
    """Result of consistency checking.

    Attributes:
        is_consistent: Whether the output is consistent with history.
        contradictions: List of detected contradictions.
        deviation_score: How much the output deviates from historical patterns (0–1).
    """

    is_consistent: bool = True
    contradictions: List[str] = field(default_factory=list)
    deviation_score: float = 0.0


class ConsistencyChecker:
    """Checks output consistency against processing history.

    Detects internal contradictions and deviations from historical patterns.

    Example:
        >>> checker = ConsistencyChecker(deviation_threshold=0.3)
        >>> result = checker.check(
        ...     {"answer": "Paris is the capital of France"},
        ...     [{"output": "Paris is the capital of France"}],
        ... )
        >>> print(result.is_consistent)
    """

    def __init__(self, deviation_threshold: float = 0.3):
        """Initialize consistency checker.

        Args:
            deviation_threshold: Threshold above which deviation is flagged.
        """
        self.deviation_threshold = deviation_threshold

    def check(self, result: Any,
              history: Optional[List[Any]] = None) -> ConsistencyResult:
        """Check output consistency against historical results.

        Args:
            result: The current output/result to check.
            history: List of previous ProcessingResult or similar objects.

        Returns:
            ConsistencyResult with contradictions and deviation score.
        """
        if history is None:
            history = []

        if not history:
            return ConsistencyResult(
                is_consistent=True,
                contradictions=[],
                deviation_score=0.0,
            )

        contradictions: List[str] = []
        current_text = self._to_text(result)

        # Check each previous result for contradictions
        for i, past in enumerate(history):
            past_text = self._to_text(past)

            # Check for direct contradictions
            if self._has_contradiction(current_text, past_text):
                contradictions.append(
                    f"Output contradicts history item {i}: "
                    f"{past_text[:80]}..."
                )

        # Compute deviation score based on contradiction ratio
        deviation_score = (
            len(contradictions) / len(history) if history else 0.0
        )
        is_consistent = deviation_score <= self.deviation_threshold

        return ConsistencyResult(
            is_consistent=is_consistent,
            contradictions=contradictions,
            deviation_score=deviation_score,
        )

    def _to_text(self, value: Any) -> str:
        """Convert a value to text for comparison."""
        if value is None:
            return ""
        if hasattr(value, "output"):
            return str(value.output)
        if isinstance(value, dict):
            return value.get("output", str(value))
        return str(value)

    def _has_contradiction(self, current: str, past: str) -> bool:
        """Detect if two texts contain a contradiction.

        Checks if removing negation markers from one text makes it
        substantially similar to the other, indicating a contradiction.
        """
        if not current or not past:
            return False

        current_lower = current.lower()
        past_lower = past.lower()

        negation_markers = ["not ", " never ", "incorrect", "wrong", "false"]
        # Check marker at end of string too
        if current_lower.endswith(" not") or current_lower.endswith(" never"):
            negation_markers.extend([" not", " never"])

        for marker in negation_markers:
            if marker in current_lower:
                # Remove the negation marker and compare
                cleaned = current_lower.replace(marker, " ")
                # Normalize whitespace
                cleaned = " ".join(cleaned.split())
                past_normalized = " ".join(past_lower.split())

                # If the cleaned text is highly similar to the past text
                # (edit distance-based), it's a contradiction
                if self._similar(cleaned, past_normalized, threshold=0.6):
                    return True

                # Also check: is the past text a substring of cleaned or vice versa
                if (past_normalized in cleaned or cleaned in past_normalized) and \
                   abs(len(cleaned) - len(past_normalized)) < 20:
                    return True

        return False

    def _similar(self, a: str, b: str, threshold: float = 0.6) -> bool:
        """Check if two strings are similar (simple word overlap)."""
        if not a or not b:
            return False
        words_a = set(a.split())
        words_b = set(b.split())
        if not words_a or not words_b:
            return False
        intersection = words_a & words_b
        union = words_a | words_b
        return len(intersection) / len(union) >= threshold
