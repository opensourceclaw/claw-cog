"""Tests for confidence exposure module."""
import pytest
from claw_cog import ConsciousAgent
from claw_cog.confidence_exposure import ConfidenceExposure, ConfidenceReport


class TestConfidenceExposure:
    def test_from_result(self):
        agent = ConsciousAgent(enable_c2=False)
        result = agent.process("test")
        report = ConfidenceExposure.from_processing_result(result)
        assert 0.0 <= report.confidence <= 1.0

    def test_format_warning(self):
        report = ConfidenceReport(confidence=0.3, level="C0", warning=True, recommendation="审核")
        formatted = ConfidenceExposure.format_for_response(report)
        assert "置信度" in formatted

    def test_format_high_confidence(self):
        report = ConfidenceReport(confidence=0.9, level="C2", warning=False)
        formatted = ConfidenceExposure.format_for_response(report)
        assert formatted == ""

    def test_decision_guidance(self):
        agent = ConsciousAgent(enable_c2=False)
        result = agent.process("important decision")
        guidance = ConfidenceExposure.get_decision_guidance(result)
        assert "confidence" in guidance
        assert "warning" in guidance
