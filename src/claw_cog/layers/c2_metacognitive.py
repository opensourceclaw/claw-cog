"""
C2: Metacognitive Layer.

Self-monitoring, goal tracking, confidence assessment.
Based on Freud's Superego and Husserl's Protention.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
import logging

from claw_cog.config.defaults import Config

if TYPE_CHECKING:
    from claw_cog.core.workspace import C1Result

logger = logging.getLogger(__name__)


@dataclass
class C2Result:
    """Result from C2 metacognitive monitoring."""

    needs_adjustment: bool
    adjustment_type: str
    confidence_estimate: float
    recommendation: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    # v1.0.0b3: enhanced monitoring fields
    performance_trend: str = "stable"
    learning_signal: float = 0.0
    attention_score: float = 0.5


@dataclass
class CompetenceAssessment:
    """MUSE-based competence assessment result."""

    score: float
    known_coverage: float
    novelty_score: float
    risk_level: str
    recommendation: str


class C2Metacognitive:
    """C2: Metacognitive Layer.

    Monitors and regulates C1 processing via:
    - Goal tracking (Superego function)
    - Confidence assessment with escalation
    - Competence awareness (MUSE framework)
    - Prediction generation (Protention)
    """

    def __init__(self, config: Config):
        self.config = config
        self._active = True
        self._confidence_thresholds = {
            "high": config.c2_high_threshold,
            "medium": config.c2_medium_threshold,
            "low": config.c2_low_threshold,
        }
        self._monitor_count: int = 0
        self._adjustment_counts: Dict[str, int] = {
            "none": 0, "strategy": 0, "confidence": 0, "seek_help": 0
        }
        self._recent_confidences: List[float] = []
        # rc.2: Sampling and caching for performance
        self._monitor_sample_rate: float = 1.0
        self._cached_result: Optional["C2Result"] = None
        self._cache_ttl: int = 0
        self._cache_counter: int = 0
        logger.debug("C2Metacognitive layer initialized")

    def monitor(self, c1_result: "C1Result", confidence_threshold: float = 0.7) -> C2Result:
        """Monitor C1 processing result and recommend adjustments."""
        self._monitor_count += 1

        # rc.2: Sampling optimization — skip full computation if sampling
        if self._monitor_sample_rate < 1.0:
            import random
            if random.random() > self._monitor_sample_rate:
                if self._cached_result is not None:
                    return self._cached_result

        # rc.2: Cache TTL — return cached result if within TTL
        if self._cache_ttl > 0 and self._cached_result is not None:
            if self._cache_counter < self._cache_ttl:
                self._cache_counter += 1
                return self._cached_result
            self._cache_counter = 0

        confidence = getattr(c1_result, "confidence", 0.5)

        if confidence >= self._confidence_thresholds["high"]:
            adj = "none"
            rec = None
        elif confidence >= self._confidence_thresholds["medium"]:
            adj = "strategy"
            rec = "gather_more_information"
        elif confidence >= self._confidence_thresholds["low"]:
            adj = "confidence"
            rec = "increase_confidence"
        else:
            adj = "seek_help"
            rec = "request_human_assistance"

        self._adjustment_counts[adj] += 1

        # Track confidences for trend analysis
        self._recent_confidences.append(confidence)
        if len(self._recent_confidences) > 10:
            self._recent_confidences.pop(0)

        # Enhanced monitoring
        trend = self._analyze_trend()
        learning = self._generate_learning_signal(confidence, trend)
        attention = 1.0 - abs(confidence - 0.5) * 2  # highest at 0.5

        result = C2Result(
            needs_adjustment=(adj != "none"),
            adjustment_type=adj,
            confidence_estimate=confidence,
            recommendation=rec,
            performance_trend=trend,
            learning_signal=learning,
            attention_score=attention,
            metadata={
                "monitor_index": self._monitor_count,
                "threshold_high": self._confidence_thresholds["high"],
                "threshold_medium": self._confidence_thresholds["medium"],
                "threshold_low": self._confidence_thresholds["low"],
            },
        )

        # rc.2: Cache full result for TTL/sampling reuse
        self._cached_result = result
        return result

    def assess_competence(
        self, situation: Any, known_situations: Optional[List[Any]] = None
    ) -> CompetenceAssessment:
        """Assess competence via MUSE framework.

        Calculates:
        - Known coverage: how many similar situations exist in memory
        - Novelty score: how different this situation is from known ones
        - Risk level based on coverage and novelty
        - Action recommendation

        Args:
            situation: Current situation (str or dict with 'description')
            known_situations: Known/historical situations for comparison

        Returns:
            CompetenceAssessment with scores and recommendation
        """
        if known_situations is None:
            known_situations = []

        # Known coverage — ratio of similar situations
        known_coverage = min(1.0, len(known_situations) / 5) if known_situations else 0.0

        # Novelty score — estimate how new/unknown this is
        if isinstance(situation, str):
            sit_len = len(situation)
            novelty_score = 1.0 - known_coverage
            if sit_len > 50:
                novelty_score *= 0.8  # Longer descriptions = more context = less novel
        elif isinstance(situation, dict):
            novelty_score = 1.0 - (known_coverage * 0.7)
        else:
            novelty_score = 1.0

        # Overall competence score
        score = max(0.0, 1.0 - novelty_score * 0.8)
        score = min(1.0, score + known_coverage * 0.2)

        # Risk level based on coverage and novelty
        if novelty_score > 0.7:
            risk_level = "high"
        elif novelty_score > 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"

        # Recommendation
        if risk_level == "high":
            recommendation = "seek_human_assistance"
        elif risk_level == "medium":
            recommendation = "proceed_with_caution"
        else:
            recommendation = "proceed_confidently"

        return CompetenceAssessment(
            score=score,
            known_coverage=known_coverage,
            novelty_score=novelty_score,
            risk_level=risk_level,
            recommendation=recommendation,
        )

    def _analyze_trend(self) -> str:
        """Analyze confidence trend from recent processing."""
        if len(self._recent_confidences) < 3:
            return "stable"

        recent = self._recent_confidences[-3:]
        if recent[-1] > recent[0] + 0.1:
            return "improving"
        elif recent[-1] < recent[0] - 0.1:
            return "declining"
        return "stable"

    def _generate_learning_signal(self, confidence: float, trend: str) -> float:
        """Generate learning signal based on confidence and trend."""
        base_signal = confidence - 0.5

        if trend == "improving":
            return base_signal + 0.2
        elif trend == "declining":
            return base_signal - 0.2
        return base_signal

    def get_monitor_stats(self) -> Dict[str, Any]:
        """Get monitoring statistics."""
        return {
            "total_monitors": self._monitor_count,
            "adjustments": dict(self._adjustment_counts),
            "trusted_ratio": (
                self._adjustment_counts["none"] / max(1, self._monitor_count)
            ),
        }

    def is_active(self) -> bool:
        return self._active

    def reset(self) -> None:
        self._monitor_count = 0
        self._adjustment_counts = {k: 0 for k in self._adjustment_counts}
        self._recent_confidences.clear()
