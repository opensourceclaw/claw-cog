"""Quality assessment for verification layer."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class QualityScore(Enum):
    """Quality score levels."""

    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


@dataclass
class QualityResult:
    """Result of quality assessment.

    Attributes:
        overall_score: Overall quality score.
        scores: Component-level score breakdown.
        details: Detailed explanation for each component.
    """

    overall_score: QualityScore = QualityScore.EXCELLENT
    scores: Dict[str, QualityScore] = field(default_factory=dict)
    details: Dict[str, str] = field(default_factory=dict)


class QualityAssessor:
    """Assesses output quality across multiple dimensions.

    Supports configurable thresholds for each quality dimension.
    Dimensions include: completeness, clarity, safety, and relevance.

    Example:
        >>> qa = QualityAssessor(completeness_threshold=0.5, safety_threshold=0.8)
        >>> result = qa.assess("The answer is 42.", context={"expected_length": 20})
        >>> print(result.overall_score)
    """

    def __init__(
        self,
        completeness_threshold: float = 0.5,
        clarity_threshold: float = 0.5,
        safety_threshold: float = 0.8,
        relevance_threshold: float = 0.5,
    ):
        self.completeness_threshold = completeness_threshold
        self.clarity_threshold = clarity_threshold
        self.safety_threshold = safety_threshold
        self.relevance_threshold = relevance_threshold

    def assess(self, output: Any,
               context: Optional[Dict] = None) -> QualityResult:
        """Assess the quality of an output across all dimensions.

        Args:
            output: The output to assess (str, list, dict, or other).
            context: Optional context with hints like expected_length.

        Returns:
            QualityResult with overall and per-dimension scores.
        """
        if context is None:
            context = {}

        scores: Dict[str, QualityScore] = {}
        details: Dict[str, str] = {}

        scores["completeness"], details["completeness"] = self._check_completeness(
            output, context
        )
        scores["clarity"], details["clarity"] = self._check_clarity(output)
        scores["safety"], details["safety"] = self._check_safety(output)
        scores["relevance"], details["relevance"] = self._check_relevance(
            output, context
        )

        # Overall score is the worst across all dimensions
        priority_order = [QualityScore.POOR, QualityScore.FAIR,
                          QualityScore.GOOD, QualityScore.EXCELLENT]
        overall = QualityScore.EXCELLENT
        for score in scores.values():
            if priority_order.index(score) < priority_order.index(overall):
                overall = score

        return QualityResult(
            overall_score=overall,
            scores=scores,
            details=details,
        )

    def _check_completeness(self, output: Any, context: Dict) -> tuple:
        """Check if output is sufficiently complete."""
        if output is None:
            return QualityScore.POOR, "Output is None"

        if isinstance(output, str):
            length = len(output)
            expected = context.get("expected_length")
            if expected is not None and length < expected:
                ratio = length / expected
                return self._score_from_ratio(ratio, self.completeness_threshold), (
                    f"Length {length} < expected {expected}"
                )
            if length == 0:
                return QualityScore.POOR, "Empty string output"
            if length < 10:
                return QualityScore.FAIR, f"Short output ({length} chars)"
            return QualityScore.EXCELLENT, f"Adequate length ({length} chars)"

        if isinstance(output, (list, dict)):
            size = len(output)
            if size == 0:
                return QualityScore.POOR, "Empty collection"
            if size <= 2:
                return QualityScore.FAIR, f"Small collection ({size} items)"
            return QualityScore.GOOD, f"Collection with {size} items"

        return QualityScore.GOOD, "Non-empty output"

    def _check_clarity(self, output: Any) -> tuple:
        """Check if output is clear and well-structured."""
        if output is None:
            return QualityScore.POOR, "Output is None"

        if isinstance(output, str):
            # Check for excessive jargon or unclear patterns
            if len(output) > 1000:
                return QualityScore.FAIR, "Output is very long, may lack clarity"
            if output.count("\n") > 20:
                return QualityScore.GOOD, "Well-structured with line breaks"
            return QualityScore.EXCELLENT, "Clear and concise"

        if isinstance(output, dict):
            return QualityScore.EXCELLENT, "Structured dict output"

        if isinstance(output, list):
            return QualityScore.GOOD, "List output"

        return QualityScore.GOOD, "Non-string output"

    def _check_safety(self, output: Any) -> tuple:
        """Check output for potential safety concerns."""
        if output is None:
            return QualityScore.EXCELLENT, "No output to check"

        text = str(output).lower()

        # High-risk patterns
        high_risk = ["password", "secret", "token", "key", "credential"]
        for pattern in high_risk:
            if pattern in text:
                return QualityScore.POOR, f"May contain sensitive data: '{pattern}'"

        # Medium-risk patterns
        medium_risk = ["private", "internal", "confidential"]
        for pattern in medium_risk:
            if pattern in text:
                return QualityScore.FAIR, f"References sensitive term: '{pattern}'"

        return QualityScore.EXCELLENT, "No safety concerns detected"

    def _check_relevance(self, output: Any, context: Dict) -> tuple:
        """Check if output is relevant to the context."""
        if output is None:
            return QualityScore.POOR, "No output to assess relevance"

        expected_topic = context.get("expected_topic")
        if expected_topic is None:
            return QualityScore.GOOD, "No relevance reference available"

        if isinstance(output, str):
            if expected_topic.lower() in output.lower():
                return QualityScore.EXCELLENT, f"Contains expected topic: {expected_topic}"
            return QualityScore.FAIR, f"Does not mention expected topic: {expected_topic}"

        return QualityScore.GOOD, "Non-string output, relevance not assessed"

    def _score_from_ratio(self, ratio: float, threshold: float) -> QualityScore:
        """Convert a ratio to a quality score based on threshold."""
        if ratio >= threshold:
            return QualityScore.GOOD
        elif ratio >= threshold * 0.5:
            return QualityScore.FAIR
        return QualityScore.POOR
