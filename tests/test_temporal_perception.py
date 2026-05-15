"""Tests for TemporalPerception module (P1-1 C0)"""

import pytest
from claw_cog.modules.temporal_perception import (
    TemporalPerception, TemporalEvent, DurationEstimate, EventType,
)
from datetime import datetime, timedelta


class TestTemporalEvent:
    def test_default_creation(self):
        event = TemporalEvent(
            event_type=EventType.INSTANTANEOUS,
            reference="now",
            confidence=0.7,
        )
        assert event.event_type == EventType.INSTANTANEOUS
        assert event.reference == "now"
        assert event.confidence == 0.7

    def test_to_dict(self):
        event = TemporalEvent(
            event_type=EventType.DURATION,
            reference="2 hours",
            duration_seconds=7200.0,
            confidence=0.8,
        )
        d = event.to_dict()
        assert d["event_type"] == "duration"
        assert d["duration_seconds"] == 7200.0
        assert d["confidence"] == 0.8

    def test_deadline_type(self):
        event = TemporalEvent(
            event_type=EventType.DEADLINE,
            reference="by Friday",
        )
        assert event.event_type == EventType.DEADLINE

    def test_recurring_type(self):
        event = TemporalEvent(
            event_type=EventType.RECURRING,
            reference="every day",
            recurrence_pattern="daily",
        )
        assert event.event_type == EventType.RECURRING
        assert event.recurrence_pattern == "daily"


class TestDurationEstimate:
    def test_default_creation(self):
        de = DurationEstimate(expected=3600.0, confidence=0.5)
        assert de.expected == 3600.0
        assert de.confidence == 0.5

    def test_range(self):
        de = DurationEstimate(expected=100.0, confidence=0.7, range_min=80.0, range_max=120.0)
        assert de.range_min == 80.0
        assert de.range_max == 120.0

    def test_to_dict(self):
        de = DurationEstimate(expected=7200.0, confidence=0.8, similar_task_count=5)
        d = de.to_dict()
        assert d["expected_seconds"] == 7200.0
        assert d["similar_task_count"] == 5


class TestTemporalPerception:
    @pytest.fixture
    def perception(self):
        return TemporalPerception()

    def test_detect_duration_english(self, perception):
        events = perception.detect_events(["meeting will take 2 hours"])
        assert len(events) >= 1
        assert events[0].event_type == EventType.DURATION
        assert events[0].duration_seconds == 7200.0

    def test_detect_duration_minutes(self, perception):
        events = perception.detect_events(["this should take 30 minutes"])
        assert len(events) >= 1
        assert events[0].event_type == EventType.DURATION
        assert events[0].duration_seconds == 1800.0

    def test_detect_duration_chinese(self, perception):
        events = perception.detect_events(["大概需要2小时完成"])
        assert len(events) >= 1
        assert events[0].event_type == EventType.DURATION

    def test_detect_recurring_daily(self, perception):
        events = perception.detect_events(["standup meeting every day"])
        assert len(events) >= 1
        assert events[0].event_type == EventType.RECURRING
        assert events[0].recurrence_pattern == "daily"

    def test_detect_recurring_weekly(self, perception):
        events = perception.detect_events(["every monday we do sprint review"])
        assert len(events) >= 1
        assert events[0].event_type == EventType.RECURRING
        assert events[0].recurrence_pattern == "weekly"

    def test_detect_recurring_chinese(self, perception):
        events = perception.detect_events(["每天都要做检查"])
        assert len(events) >= 1
        assert events[0].event_type == EventType.RECURRING

    def test_detect_deadline(self, perception):
        events = perception.detect_events(["please finish by tomorrow"])
        assert len(events) >= 1
        assert events[0].event_type == EventType.DEADLINE

    def test_detect_instantaneous(self, perception):
        events = perception.detect_events(["do this right now!"])
        assert len(events) >= 1
        assert events[0].event_type == EventType.INSTANTANEOUS

    def test_detect_chinese_instant(self, perception):
        events = perception.detect_events(["马上处理"])
        assert len(events) >= 1
        assert events[0].event_type == EventType.INSTANTANEOUS

    def test_detect_multiple_inputs(self, perception):
        events = perception.detect_events([
            "standup every day",
            "code review takes 30 minutes",
            "finish by tomorrow",
        ])
        assert len(events) == 3

    def test_detect_empty_input(self, perception):
        events = perception.detect_events([""])
        assert len(events) == 0

    def test_no_event_text(self, perception):
        events = perception.detect_events(["the weather is nice today"])
        assert len(events) == 0

    def test_estimate_duration_default(self, perception):
        task = {"type": "development"}
        estimate = perception.estimate_duration(task)
        assert estimate.expected == 7200.0
        assert estimate.confidence == 0.3

    def test_estimate_duration_with_history(self, perception):
        task = {"type": "development"}
        similar = [
            {"type": "development", "duration": 3600.0},
            {"type": "development", "duration": 5400.0},
            {"type": "development", "duration": 4500.0},
        ]
        estimate = perception.estimate_duration(task, similar)
        assert 4000.0 <= estimate.expected <= 5000.0  # Should be ~4500
        assert estimate.confidence > 0.3
        assert estimate.similar_task_count == 3

    def test_estimate_duration_unknown_type(self, perception):
        task = {"type": "unknown_type"}
        estimate = perception.estimate_duration(task)
        assert estimate.expected == 3600.0  # Default fallback

    def test_recognize_sequences(self, perception):
        events = [
            TemporalEvent(EventType.INSTANTANEOUS, "first", start_time=datetime(2025, 1, 1, 10, 0)),
            TemporalEvent(EventType.INSTANTANEOUS, "second", start_time=datetime(2025, 1, 1, 9, 0)),
        ]
        sequences = perception.recognize_sequences(events)
        assert len(sequences) >= 1

    def test_get_history(self, perception):
        perception.detect_events(["every day", "2 hours"])
        history = perception.get_history()
        assert len(history) >= 1

    def test_clear_history(self, perception):
        perception.detect_events(["every day"])
        perception.clear_history()
        assert len(perception.get_history()) == 0

    def test_get_statistics(self, perception):
        perception.detect_events(["2 hours", "every day"])
        stats = perception.get_statistics()
        assert stats["events_detected"] >= 1

    def test_detect_duration_days(self, perception):
        events = perception.detect_events(["this will take 3 days"])
        assert len(events) >= 1
        assert events[0].event_type == EventType.DURATION
        assert events[0].duration_seconds == 3 * 86400

    def test_detect_duration_weeks(self, perception):
        events = perception.detect_events(["sprint lasts 2 weeks"])
        assert len(events) >= 1
        assert events[0].event_type == EventType.DURATION

    def test_estimate_duration_empty_similar(self, perception):
        task = {"type": "testing"}
        estimate = perception.estimate_duration(task, [])
        assert estimate.expected == 3600.0  # testing default
