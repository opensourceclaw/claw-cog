"""Tests for volition engine (coverage boost)."""

import pytest
from claw_cog.layers.c2_metacognitive import C2Result
from claw_cog.modules.volition.engine import VolitionEngine
from claw_cog.modules.volition.goal_tracker import GoalTracker
from claw_cog.modules.volition.intention_buffer import IntentionBuffer
from claw_cog.modules.volition.types import Goal, GoalPriority


class TestVolitionEngine:
    @pytest.fixture
    def engine(self):
        tracker = GoalTracker()
        buf = IntentionBuffer()
        return VolitionEngine(tracker, buf, memory=None)

    def test_generate_goals(self, engine):
        c2 = C2Result(needs_adjustment=True, adjustment_type="strategy",
                      confidence_estimate=0.4, recommendation="gather_more_info")
        goals = engine.generate_goals(c2)
        assert isinstance(goals, list)
        assert len(goals) > 0

    def test_generate_goals_seek_help(self, engine):
        c2 = C2Result(needs_adjustment=True, adjustment_type="seek_help",
                      confidence_estimate=0.2, recommendation="ask_human")
        goals = engine.generate_goals(c2)
        assert len(goals) > 0

    def test_select_intention(self, engine):
        goals = [
            Goal(goal_id="g1", description="task1", priority=GoalPriority.HIGH, source="test"),
            Goal(goal_id="g2", description="task2", priority=GoalPriority.MEDIUM, source="test"),
        ]
        intention = engine.select_intention(goals)
        assert intention is not None
        assert intention.goal_id in ["g1", "g2"]

    def test_select_intention_empty(self, engine):
        assert engine.select_intention([]) is None

    def test_get_statistics(self, engine):
        stats = engine.get_statistics()
        assert isinstance(stats, dict)

    def test_clear(self, engine):
        c2 = C2Result(needs_adjustment=True, adjustment_type="low_confidence",
                      confidence_estimate=0.3)
        engine.generate_goals(c2)
        engine.clear()

    @staticmethod
    def test_infer_priority_static():
        c2 = C2Result(needs_adjustment=True, adjustment_type="seek_help",
                      confidence_estimate=0.2)
        priority = VolitionEngine._infer_priority(c2)
        assert priority == GoalPriority.CRITICAL
