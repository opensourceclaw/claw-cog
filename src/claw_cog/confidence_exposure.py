"""Confidence Exposure — user-visible confidence from claw-cog v1.5.0."""

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


@dataclass
class ConfidenceReport:
    """User-visible confidence report."""
    confidence: float
    level: str
    recommendation: str = ""
    warning: bool = False


class ConfidenceExposure:
    """Exposes claw-cog confidence levels for user-facing decisions.

    Integrates with Friday to display confidence in responses
    and warn users when the agent is uncertain.
    """

    @staticmethod
    def from_processing_result(result: Any) -> ConfidenceReport:
        """Create a confidence report from a ProcessingResult."""
        conf = getattr(result, "confidence", 0.5)
        level = getattr(result, "level", None)
        level_name = level.name if hasattr(level, "name") else str(level)

        rec = ""
        warning = False
        if conf < 0.3:
            rec = "强烈建议人工审核"
            warning = True
        elif conf < 0.5:
            rec = "建议验证结果"
            warning = True
        elif conf < 0.8:
            rec = "可参考但需留意边界情况"
        else:
            rec = "高置信度，可直接采纳"

        return ConfidenceReport(
            confidence=round(conf, 2),
            level=level_name,
            recommendation=rec,
            warning=warning,
        )

    @staticmethod
    def format_for_response(report: ConfidenceReport) -> str:
        """Format confidence as a user-visible string."""
        if report.warning:
            return f"[置信度: {report.confidence:.0%}, {report.recommendation}]"
        if report.confidence < 0.8:
            return f"[置信度: {report.confidence:.0%}]"
        return ""

    @staticmethod
    def get_decision_guidance(result: Any) -> Dict[str, Any]:
        """Get structured decision guidance from processing result."""
        report = ConfidenceExposure.from_processing_result(result)
        return {
            "confidence": report.confidence,
            "level": report.level,
            "recommendation": report.recommendation,
            "warning": report.warning,
            "formatted": ConfidenceExposure.format_for_response(report),
        }
