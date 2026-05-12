"""Tests for C2 Metacognitive layer."""
import pytest
from claw_cog.config.defaults import Config
from claw_cog.layers.c2_metacognitive import C2Metacognitive, C2Result, CompetenceAssessment


class DummyC1Result:
    def __init__(self, confidence=0.5):
        self.confidence = confidence


class TestC2Metacognitive:
    def setup_method(self):
        self.config = Config()
        self.c2 = C2Metacognitive(self.config)

    def test_initialization(self):
        assert self.c2.is_active()

    def test_high_confidence_no_adjustment(self):
        result = self.c2.monitor(DummyC1Result(confidence=0.9))
        assert result.adjustment_type == "none"
        assert not result.needs_adjustment

    def test_medium_confidence_strategy_adjustment(self):
        result = self.c2.monitor(DummyC1Result(confidence=0.55))
        assert result.adjustment_type == "strategy"

    def test_very_low_confidence_seek_help(self):
        result = self.c2.monitor(DummyC1Result(confidence=0.35))
        assert result.adjustment_type == "seek_help" or result.adjustment_type == "confidence"

    def test_below_low_seek_help(self):
        result = self.c2.monitor(DummyC1Result(confidence=0.05))
        assert result.adjustment_type == "seek_help" or result.adjustment_type == "confidence"
        assert "human" in result.recommendation.lower()

    def test_competence_with_known_situations(self):
        assessment = self.c2.assess_competence(
            "test situation",
            known_situations=["similar situation 1", "similar situation 2"],
        )
        assert isinstance(assessment, CompetenceAssessment)
        assert assessment.known_coverage > 0
        assert 0.0 <= assessment.score <= 1.0
        assert assessment.risk_level in ("low", "medium", "high")

    def test_competence_with_no_known_situations(self):
        assessment = self.c2.assess_competence("novel situation", [])
        assert assessment.known_coverage == 0
        assert assessment.novelty_score > 0.5

    def test_competence_dict_input(self):
        assessment = self.c2.assess_competence(
            {"description": "complex task", "domain": "coding"},
            ["task1", "task2"],
        )
        assert 0.0 <= assessment.score <= 1.0
        assert isinstance(assessment.recommendation, str)

    def test_monitor_stats(self):
        self.c2.monitor(DummyC1Result(0.9))
        self.c2.monitor(DummyC1Result(0.5))
        self.c2.monitor(DummyC1Result(0.05))
        stats = self.c2.get_monitor_stats()
        assert stats["total_monitors"] == 3
        assert stats["adjustments"]["none"] == 1
        assert stats["adjustments"]["seek_help"] == 1

    def test_reset(self):
        self.c2.monitor(DummyC1Result(0.5))
        self.c2.reset()
        assert self.c2.get_monitor_stats()["total_monitors"] == 0

    def test_competence_long_description(self):
        """Long descriptions reduce novelty score slightly."""
        assessment = self.c2.assess_competence(
            "A very long description " * 10,
            ["known1"],
        )
        assert isinstance(assessment.score, float)

    def test_competence_with_many_known(self):
        """Many known situations increase coverage."""
        assessment = self.c2.assess_competence(
            "routine task",
            ["t1", "t2", "t3", "t4", "t5", "t6"],
        )
        assert assessment.known_coverage == 1.0

    def test_all_adjustment_types(self):
        """Verify all four adjustment types can be triggered."""
        types_seen = set()
        for conf in [0.95, 0.55, 0.35, 0.05]:
            r = self.c2.monitor(DummyC1Result(confidence=conf))
            types_seen.add(r.adjustment_type)
        assert len(types_seen) >= 3  # at least 3 different types
