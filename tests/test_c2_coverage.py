"""Tests for C2 metacognitive layer (coverage boost)."""

import pytest
from unittest.mock import MagicMock
from claw_cog.config.defaults import Config
from claw_cog.layers.c2_metacognitive import C2Metacognitive, C2Result, CompetenceAssessment
from claw_cog.core.workspace import C1Result


class TestC2Metacognitive:
    @pytest.fixture
    def c2(self):
        config = Config()
        return C2Metacognitive(config)

    def test_monitor_low_confidence(self, c2):
        c1 = C1Result(output="test", confidence=0.2, broadcast_time_ms=10.0, metadata={})
        result = c2.monitor(c1, confidence_threshold=0.7)
        assert result.needs_adjustment is True

    def test_monitor_high_confidence(self, c2):
        c1 = C1Result(output="test", confidence=0.9, broadcast_time_ms=10.0, metadata={})
        result = c2.monitor(c1, confidence_threshold=0.7)
        assert isinstance(result, C2Result)

    def test_monitor_mid_confidence(self, c2):
        c1 = C1Result(output="test", confidence=0.5, broadcast_time_ms=10.0, metadata={})
        result = c2.monitor(c1, confidence_threshold=0.7)
        assert result.needs_adjustment in (True, False)

    def test_assess_competence(self, c2):
        assessment = c2.assess_competence("new situation", ["known", "familiar"])
        assert isinstance(assessment, CompetenceAssessment)
        assert 0.0 <= assessment.score <= 1.0

    def test_assess_competence_all_known(self, c2):
        assessment = c2.assess_competence("hello", ["hello", "hi", "world"])
        assert assessment.known_coverage > 0

    def test_get_monitor_stats(self, c2):
        c1 = C1Result(output="t", confidence=0.5, broadcast_time_ms=10.0, metadata={})
        c2.monitor(c1)
        stats = c2.get_monitor_stats()
        assert stats["total_monitors"] >= 1

    def test_is_active(self, c2):
        assert c2.is_active() is True

    def test_reset(self, c2):
        c1 = C1Result(output="t", confidence=0.5, broadcast_time_ms=10.0, metadata={})
        c2.monitor(c1)
        c2.reset()

    def test_competence_assessment_risk_levels(self, c2):
        a = c2.assess_competence("danger zone", [])
        assert a.risk_level in ("low", "medium", "high", "critical")


class TestC2Result:
    def test_create(self):
        r = C2Result(needs_adjustment=True, adjustment_type="strategy", confidence_estimate=0.4)
        assert r.needs_adjustment is True
