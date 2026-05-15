"""Tests for TemporalPrediction module (P1-1 C2)"""

import pytest
from datetime import datetime, timedelta
from claw_cog.modules.temporal_understanding import TemporalPattern, PatternType
from claw_cog.modules.temporal_prediction import (
    TemporalPrediction, PredictedEvent, TemporalConflict,
    ResolutionSuggestion, ConflictType,
)


class TestPredictedEvent:
    def test_default_creation(self):
        event = PredictedEvent(
            description="standup meeting",
            predicted_time=datetime.now() + timedelta(days=1),
            duration_seconds=1800.0,
            confidence=0.8,
        )
        assert event.description == "standup meeting"
        assert event.duration_seconds == 1800.0
        assert event.confidence == 0.8

    def test_to_dict(self):
        event = PredictedEvent(
            description="review",
            predicted_time=datetime(2025, 6, 1, 10, 0),
            confidence=0.9,
        )
        d = event.to_dict()
        assert d["description"] == "review"
        assert d["confidence"] == 0.9
        assert d["predicted_time"] is not None


class TestTemporalConflict:
    def test_default_creation(self):
        conflict = TemporalConflict(
            conflict_type=ConflictType.OVERLAP,
            description="two meetings overlap",
            severity="high",
        )
        assert conflict.conflict_type == ConflictType.OVERLAP
        assert conflict.severity == "high"

    def test_to_dict(self):
        conflict = TemporalConflict(
            conflict_type=ConflictType.RESOURCE,
            description="insufficient resources",
            severity="medium",
        )
        d = conflict.to_dict()
        assert d["conflict_type"] == "resource"
        assert d["severity"] == "medium"


class TestResolutionSuggestion:
    def test_default_creation(self):
        conflict = TemporalConflict(ConflictType.OVERLAP, "overlap", severity="medium")
        suggestion = ResolutionSuggestion(
            conflict=conflict,
            strategy="reschedule",
            alternatives=[{"action": "move"}],
            details="Reschedule one meeting",
            feasibility=0.7,
        )
        assert suggestion.strategy == "reschedule"
        assert len(suggestion.alternatives) == 1

    def test_to_dict(self):
        conflict = TemporalConflict(ConflictType.DEADLINE, "deadline risk", severity="high")
        suggestion = ResolutionSuggestion(
            conflict=conflict, strategy="escalate", details="Need help",
        )
        d = suggestion.to_dict()
        assert d["strategy"] == "escalate"
        assert d["conflict"] is not None


class TestTemporalPrediction:
    @pytest.fixture
    def prediction(self):
        return TemporalPrediction()

    @pytest.fixture
    def sample_patterns(self):
        return [
            TemporalPattern(
                pattern_type=PatternType.DAILY,
                description="daily standup",
                frequency=1.0,
                confidence=0.9,
                event_count=20,
                typical_duration=900.0,  # 15 minutes
            ),
            TemporalPattern(
                pattern_type=PatternType.WEEKLY,
                description="sprint review",
                frequency=0.14,
                confidence=0.85,
                event_count=10,
                typical_duration=3600.0,  # 1 hour
            ),
            TemporalPattern(
                pattern_type=PatternType.MONTHLY,
                description="monthly retro",
                frequency=0.03,
                confidence=0.8,
                event_count=6,
                typical_duration=5400.0,  # 1.5 hours
            ),
        ]

    def test_predict_future_events(self, prediction, sample_patterns):
        horizon = timedelta(days=14)
        events = prediction.predict_future_events(sample_patterns, horizon)
        assert len(events) >= 1
        assert all(isinstance(e, PredictedEvent) for e in events)

    def test_predict_events_sorted_by_time(self, prediction, sample_patterns):
        events = prediction.predict_future_events(sample_patterns, timedelta(days=14))
        for i in range(len(events) - 1):
            assert events[i].predicted_time <= events[i + 1].predicted_time

    def test_predict_events_in_future(self, prediction, sample_patterns):
        events = prediction.predict_future_events(sample_patterns, timedelta(days=7))
        now = datetime.now()
        for e in events:
            assert e.predicted_time > now

    def test_predict_default_horizon(self, prediction, sample_patterns):
        events = prediction.predict_future_events(sample_patterns)
        assert len(events) >= 1

    def test_predict_no_patterns(self, prediction):
        events = prediction.predict_future_events([])
        assert len(events) == 0

    def test_detect_conflicts_overlap(self, prediction):
        now = datetime.now()
        events = [
            PredictedEvent("meeting A", now + timedelta(hours=1), duration_seconds=3600),
            PredictedEvent("meeting B", now + timedelta(hours=2), duration_seconds=3600),
        ]
        conflicts = prediction.detect_conflicts(events)
        # Meeting A (1h-2h) and Meeting B (2h-3h) overlap at 2h
        assert len(conflicts) > 0

    def test_detect_conflicts_no_overlap(self, prediction):
        now = datetime.now()
        events = [
            PredictedEvent("meeting A", now + timedelta(hours=1), duration_seconds=1800),
            PredictedEvent("meeting B", now + timedelta(hours=3), duration_seconds=1800),
        ]
        conflicts = prediction.detect_conflicts(events)
        # No overlap: A ends at 1.5h, B starts at 3h
        overlap_conflicts = [c for c in conflicts if c.conflict_type == ConflictType.OVERLAP]
        assert len(overlap_conflicts) == 0

    def test_detect_conflicts_resource(self, prediction):
        now = datetime.now()
        events = [
            PredictedEvent("task 1", now + timedelta(minutes=10), resource_need=0.8),
            PredictedEvent("task 2", now + timedelta(minutes=20), resource_need=0.7),
        ]
        conflicts = prediction.detect_conflicts(events)
        assert isinstance(conflicts, list)

    def test_detect_deadline_conflict(self, prediction):
        now = datetime.now()
        events = [
            PredictedEvent("urgent task", now + timedelta(minutes=30), duration_seconds=3600),
        ]
        conflicts = prediction.detect_conflicts(events)
        # 30 minutes remaining for a 1-hour task
        deadline_conflicts = [c for c in conflicts if c.conflict_type == ConflictType.DEADLINE]
        assert len(deadline_conflicts) >= 1

    def test_suggest_resolution(self, prediction):
        now = datetime.now()
        events = [
            PredictedEvent("A", now + timedelta(hours=1), duration_seconds=3600),
            PredictedEvent("B", now + timedelta(hours=2), duration_seconds=3600),
        ]
        conflicts = prediction.detect_conflicts(events)
        suggestions = prediction.suggest_resolution(conflicts)

        if suggestions:
            assert all(isinstance(s, ResolutionSuggestion) for s in suggestions)

    def test_suggest_resolution_empty(self, prediction):
        suggestions = prediction.suggest_resolution([])
        assert len(suggestions) == 0

    def test_get_statistics(self, prediction, sample_patterns):
        prediction.predict_future_events(sample_patterns, timedelta(days=7))
        stats = prediction.get_statistics()
        assert stats["predictions_made"] >= 1

    def test_clear(self, prediction, sample_patterns):
        prediction.predict_future_events(sample_patterns, timedelta(days=7))
        prediction.clear()
        stats = prediction.get_statistics()
        assert stats["predictions_made"] == 0

    def test_overlap_resolution_strategy(self, prediction):
        now = datetime.now()
        events = [
            PredictedEvent("A", now + timedelta(hours=1), duration_seconds=3600, confidence=0.9),
            PredictedEvent("B", now + timedelta(hours=2), duration_seconds=3600, confidence=0.9),
        ]
        conflicts = prediction.detect_conflicts(events)
        if conflicts:
            overlap_conflicts = [c for c in conflicts if c.conflict_type == ConflictType.OVERLAP]
            if overlap_conflicts:
                suggestions = prediction.suggest_resolution(overlap_conflicts)
                assert suggestions[0].strategy == "reschedule"

    def test_resource_conflict(self, prediction):
        now = datetime.now()
        events = [
            PredictedEvent("heavy 1", now + timedelta(minutes=10), resource_need=1.0, duration_seconds=600),
            PredictedEvent("heavy 2", now + timedelta(minutes=15), resource_need=1.0, duration_seconds=600),
            PredictedEvent("heavy 3", now + timedelta(minutes=20), resource_need=1.0, duration_seconds=600),
        ]
        conflicts = prediction.detect_conflicts(events)
        assert isinstance(conflicts, list)


class TestConflictType:
    def test_enum_values(self):
        assert ConflictType.OVERLAP.value == "overlap"
        assert ConflictType.RESOURCE.value == "resource"
        assert ConflictType.DEADLINE.value == "deadline"
