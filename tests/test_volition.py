"""Tests for Volition layer (v1.8.0): VolitionEngine, GoalTracker, IntentionBuffer."""

import pytest
from unittest.mock import Mock

from claw_cog.modules.volition.types import (
    Goal, GoalPriority, GoalStatus, Intention, IntentionConflict,
)
from claw_cog.modules.volition.goal_tracker import GoalTracker
from claw_cog.modules.volition.intention_buffer import IntentionBuffer
from claw_cog.modules.volition.engine import VolitionEngine
from claw_cog.layers.c2_metacognitive import C2Result


class TestGoal:
    def test_default_creation(self):
        goal = Goal(
            goal_id="g1",
            description="Improve code quality",
            priority=GoalPriority.HIGH,
            source="c2_recommendation",
        )
        assert goal.goal_id == "g1"
        assert goal.description == "Improve code quality"
        assert goal.priority == GoalPriority.HIGH
        assert goal.status == GoalStatus.PENDING
        assert goal.progress == 0.0

    def test_to_dict(self):
        goal = Goal(
            goal_id="g2",
            description="Write tests",
            priority=GoalPriority.MEDIUM,
            source="test",
            parent_goal_id="g1",
        )
        d = goal.to_dict()
        assert d["goal_id"] == "g2"
        assert d["description"] == "Write tests"
        assert d["priority"] == "medium"
        assert d["source"] == "test"
        assert d["parent_goal_id"] == "g1"
        assert d["status"] == "pending"

    def test_metadata(self):
        goal = Goal(
            goal_id="g3",
            description="Meta goal",
            priority=GoalPriority.LOW,
            source="test",
            metadata={"confidence": 0.8},
        )
        assert goal.metadata["confidence"] == 0.8


class TestGoalPriority:
    def test_all_priority_levels(self):
        assert GoalPriority.LOW.value == "low"
        assert GoalPriority.MEDIUM.value == "medium"
        assert GoalPriority.HIGH.value == "high"
        assert GoalPriority.CRITICAL.value == "critical"


class TestGoalStatus:
    def test_all_statuses(self):
        assert GoalStatus.PENDING.value == "pending"
        assert GoalStatus.ACTIVE.value == "active"
        assert GoalStatus.COMPLETED.value == "completed"
        assert GoalStatus.ABANDONED.value == "abandoned"


class TestIntention:
    def test_default_creation(self):
        intention = Intention(
            intention_id="i1",
            goal_id="g1",
            action="Improve code quality",
            confidence=0.9,
            priority=GoalPriority.HIGH,
        )
        assert intention.intention_id == "i1"
        assert intention.goal_id == "g1"
        assert intention.action == "Improve code quality"
        assert intention.confidence == 0.9
        assert intention.priority == GoalPriority.HIGH

    def test_to_dict(self):
        intention = Intention(
            intention_id="i2",
            goal_id="g2",
            action="Write tests",
            confidence=0.7,
            priority=GoalPriority.MEDIUM,
        )
        d = intention.to_dict()
        assert d["intention_id"] == "i2"
        assert d["goal_id"] == "g2"
        assert d["action"] == "Write tests"
        assert d["confidence"] == 0.7
        assert d["priority"] == "medium"


class TestIntentionConflict:
    def test_default_creation(self):
        a = Intention("i1", "g1", "Task A", 0.9, GoalPriority.HIGH)
        b = Intention("i2", "g2", "Task B", 0.8, GoalPriority.MEDIUM)
        conflict = IntentionConflict(
            intention1=a,
            intention2=b,
            conflict_type="priority_inversion",
            description="Test conflict",
            severity=0.5,
        )
        assert conflict.intention1 == a
        assert conflict.intention2 == b
        assert conflict.conflict_type == "priority_inversion"
        assert conflict.severity == 0.5

    def test_to_dict(self):
        a = Intention("i1", "g1", "Task A", 0.9, GoalPriority.HIGH)
        b = Intention("i2", "g2", "Task B", 0.8, GoalPriority.MEDIUM)
        conflict = IntentionConflict(a, b, "test", "desc", 0.3)
        d = conflict.to_dict()
        assert "intention1" in d
        assert "intention2" in d
        assert d["conflict_type"] == "test"


class TestGoalTracker:
    def setup_method(self):
        self.tracker = GoalTracker(max_goals=5)

    def test_add_goal(self):
        goal = Goal("g1", "Learn Python", GoalPriority.MEDIUM, "test")
        self.tracker.add(goal)
        assert self.tracker.get("g1") == goal
        stats = self.tracker.get_statistics()
        assert stats["goals_created"] == 1
        assert stats["total_count"] == 1

    def test_get_active_returns_pending_and_active(self):
        self.tracker.add(Goal("g1", "Goal 1", GoalPriority.HIGH, "test"))
        self.tracker.add(Goal("g2", "Goal 2", GoalPriority.LOW, "test"))
        active = self.tracker.get_active()
        assert len(active) == 2
        assert active[0].priority == GoalPriority.HIGH  # sorted by priority

    def test_get_active_excludes_completed_and_abandoned(self):
        self.tracker.add(Goal("g1", "Goal 1", GoalPriority.HIGH, "test"))
        self.tracker.add(Goal("g2", "Goal 2", GoalPriority.LOW, "test"))
        self.tracker.complete("g1")
        self.tracker.abandon("g2")
        active = self.tracker.get_active()
        assert len(active) == 0

    def test_complete_goal(self):
        self.tracker.add(Goal("g1", "Goal 1", GoalPriority.MEDIUM, "test"))
        result = self.tracker.complete("g1")
        assert result is not None
        assert result.status == GoalStatus.COMPLETED
        assert result.progress == 1.0
        assert self.tracker.get_statistics()["goals_completed"] == 1

    def test_abandon_goal(self):
        self.tracker.add(Goal("g1", "Goal 1", GoalPriority.MEDIUM, "test"))
        result = self.tracker.abandon("g1")
        assert result is not None
        assert result.status == GoalStatus.ABANDONED
        assert self.tracker.get_statistics()["goals_abandoned"] == 1

    def test_update_goal_fields(self):
        self.tracker.add(Goal("g1", "Initial desc", GoalPriority.LOW, "test"))
        updated = self.tracker.update("g1", description="New desc", priority=GoalPriority.HIGH, progress=0.5)
        assert updated is not None
        assert updated.description == "New desc"
        assert updated.priority == GoalPriority.HIGH
        assert updated.progress == 0.5

    def test_update_nonexistent_goal(self):
        result = self.tracker.update("nonexistent", description="Test")
        assert result is None

    def test_get_nonexistent_goal(self):
        assert self.tracker.get("nonexistent") is None

    def test_decompose_goal(self):
        parent = Goal("g-pr", "Big task", GoalPriority.HIGH, "test")
        sub_goals = GoalTracker.decompose(parent, ["Sub A", "Sub B", "Sub C"])
        assert len(sub_goals) == 3
        for sg in sub_goals:
            assert sg.parent_goal_id == "g-pr"
            assert sg.priority == GoalPriority.HIGH

    def test_max_goals_eviction(self):
        tracker = GoalTracker(max_goals=3)
        tracker.add(Goal("g1", "G1", GoalPriority.LOW, "test"))
        tracker.add(Goal("g2", "G2", GoalPriority.LOW, "test"))
        tracker.add(Goal("g3", "G3", GoalPriority.LOW, "test"))
        tracker.add(Goal("g4", "G4", GoalPriority.HIGH, "test"))
        # Eviction marks a goal as ABANDONED but keeps it in the tracker
        stats = tracker.get_statistics()
        assert stats["goals_abandoned"] >= 1
        # Active goals should be <= max_goals
        active = tracker.get_active()
        assert len(active) <= 3

    def test_clear(self):
        self.tracker.add(Goal("g1", "Test", GoalPriority.LOW, "test"))
        self.tracker.clear()
        assert len(self.tracker.get_all()) == 0
        stats = self.tracker.get_statistics()
        assert stats["goals_created"] == 0
        assert stats["total_count"] == 0

    def test_statistics_active_count(self):
        self.tracker.add(Goal("g1", "G1", GoalPriority.LOW, "test"))
        self.tracker.add(Goal("g2", "G2", GoalPriority.LOW, "test"))
        self.tracker.complete("g1")
        stats = self.tracker.get_statistics()
        assert stats["active_count"] == 1


class TestIntentionBuffer:
    def setup_method(self):
        self.buffer = IntentionBuffer(max_size=3)

    def test_push_and_get_next(self):
        intention = Intention("i1", "g1", "Action", 0.8, GoalPriority.MEDIUM)
        self.buffer.push(intention)
        next_int = self.buffer.get_next()
        assert next_int == intention

    def test_get_next_returns_highest_priority(self):
        low = Intention("i1", "g1", "Low prio", 0.9, GoalPriority.LOW)
        high = Intention("i2", "g2", "High prio", 0.7, GoalPriority.HIGH)
        self.buffer.push(low)
        self.buffer.push(high)
        assert self.buffer.get_next().priority == GoalPriority.HIGH

    def test_get_next_empty_buffer(self):
        assert self.buffer.get_next() is None

    def test_buffer_max_size_eviction(self):
        self.buffer.push(Intention("i1", "g1", "A1", 0.5, GoalPriority.LOW))
        self.buffer.push(Intention("i2", "g2", "A2", 0.5, GoalPriority.LOW))
        self.buffer.push(Intention("i3", "g3", "A3", 0.5, GoalPriority.LOW))
        self.buffer.push(Intention("i4", "g4", "A4", 0.5, GoalPriority.LOW))
        # Oldest (i1) should be evicted
        next_int = self.buffer.get_next()
        assert next_int is not None
        assert "i1" not in [n.intention_id for n in self.buffer._buffer]

    def test_detect_conflicts_same_goal_no_conflict(self):
        self.buffer.push(Intention("i1", "g1", "A", 0.9, GoalPriority.HIGH))
        self.buffer.push(Intention("i2", "g1", "B", 0.5, GoalPriority.LOW))
        conflicts = self.buffer.detect_conflicts()
        assert len(conflicts) == 0

    def test_detect_conflicts_priority_inversion(self):
        # Low priority with high confidence, high priority with low confidence
        self.buffer.push(Intention("i1", "g1", "LowA", 0.9, GoalPriority.LOW))
        self.buffer.push(Intention("i2", "g2", "HighB", 0.3, GoalPriority.HIGH))
        conflicts = self.buffer.detect_conflicts()
        assert len(conflicts) >= 1
        assert conflicts[0].conflict_type == "priority_inversion"

    def test_clear(self):
        self.buffer.push(Intention("i1", "g1", "A", 0.5, GoalPriority.LOW))
        self.buffer.clear()
        assert self.buffer.get_next() is None
        assert self.buffer.get_statistics()["buffer_size"] == 0


class TestVolitionEngine:
    def setup_method(self):
        self.tracker = GoalTracker(max_goals=10)
        self.buffer = IntentionBuffer(max_size=5)
        self.engine = VolitionEngine(
            goal_tracker=self.tracker,
            intention_buffer=self.buffer,
            memory=None,
        )

    def test_generate_goals_from_c2_recommendation(self):
        c2 = C2Result(
            needs_adjustment=False,
            adjustment_type="none",
            confidence_estimate=0.85,
            recommendation="Continue current approach",
            performance_trend="improving",
            learning_signal=0.2,
        )
        goals = self.engine.generate_goals(c2)
        assert len(goals) >= 1
        assert goals[0].description == "Continue current approach"
        assert goals[0].source == "c2_recommendation"

    def test_generate_goals_from_adjustment(self):
        c2 = C2Result(
            needs_adjustment=True,
            adjustment_type="seek_help",
            confidence_estimate=0.2,
            recommendation="Seek assistance",
        )
        goals = self.engine.generate_goals(c2)
        # Should have main goal + adjustment goal
        assert len(goals) >= 2
        adj_goals = [g for g in goals if g.priority == GoalPriority.HIGH]
        assert len(adj_goals) >= 1

    def test_generate_goals_with_none_c2(self):
        goals = self.engine.generate_goals(None)
        assert len(goals) == 0

    def test_generate_goals_no_recommendation(self):
        c2 = C2Result(
            needs_adjustment=False,
            adjustment_type="none",
            confidence_estimate=0.5,
            recommendation=None,
        )
        goals = self.engine.generate_goals(c2)
        assert len(goals) == 0

    def test_priority_from_c2_confidence(self):
        c2 = C2Result(
            needs_adjustment=False,
            adjustment_type="none",
            confidence_estimate=0.25,
            recommendation="Very uncertain",
        )
        goals = self.engine.generate_goals(c2)
        assert len(goals) >= 1
        assert goals[0].priority == GoalPriority.HIGH

    def test_select_intention_from_goals(self):
        self.tracker.add(Goal("g1", "Action needed", GoalPriority.HIGH, "test"))
        goals = self.tracker.get_active()
        intention = self.engine.select_intention(goals)
        assert intention is not None
        assert intention.goal_id == "g1"
        assert intention.action == "Action needed"
        assert intention.priority == GoalPriority.HIGH

    def test_select_intention_empty_goals(self):
        intention = self.engine.select_intention([])
        assert intention is None

    def test_engine_statistics(self):
        c2 = C2Result(
            needs_adjustment=True,
            adjustment_type="confidence",
            confidence_estimate=0.4,
            recommendation="Adjust confidence threshold",
        )
        self.engine.generate_goals(c2)
        goals = self.tracker.get_active()
        self.engine.select_intention(goals)
        stats = self.engine.get_statistics()
        assert stats["goals_generated"] >= 1
        assert "tracker" in stats
        assert "buffer" in stats

    def test_engine_clear(self):
        c2 = C2Result(
            needs_adjustment=False,
            adjustment_type="none",
            confidence_estimate=0.5,
            recommendation="Test goal",
        )
        self.engine.generate_goals(c2)
        self.engine.clear()
        stats = self.engine.get_statistics()
        assert stats["goals_generated"] == 0
        assert stats["tracker"]["total_count"] == 0
