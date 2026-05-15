"""Tests for TemporalUnderstanding module (P1-1 C1)"""

import pytest
from datetime import datetime, timedelta
from claw_cog.modules.temporal_perception import TemporalEvent, EventType
from claw_cog.modules.temporal_understanding import (
    TemporalUnderstanding, TemporalPattern, ScheduleEntry,
    DeadlineInfo, PatternType,
)


class TestTemporalPattern:
    def test_default_creation(self):
        pattern = TemporalPattern(
            pattern_type=PatternType.DAILY,
            description="daily standup",
            frequency=1.0,
            confidence=0.8,
            event_count=20,
        )
        assert pattern.pattern_type == PatternType.DAILY
        assert pattern.frequency == 1.0
        assert pattern.event_count == 20

    def test_to_dict(self):
        pattern = TemporalPattern(
            pattern_type=PatternType.WEEKLY,
            description="weekly review",
            frequency=0.5,
            confidence=0.7,
            typical_duration=1800.0,
        )
        d = pattern.to_dict()
        assert d["pattern_type"] == "weekly"
        assert d["frequency"] == 0.5
        assert d["typical_duration"] == 1800.0


class TestScheduleEntry:
    def test_default_creation(self):
        pattern = TemporalPattern(PatternType.DAILY, "test", 1.0, 0.8)
        entry = ScheduleEntry(
            pattern=pattern,
            suggested_time="09:00",
            flexibility=0.5,
            priority=3,
        )
        assert entry.suggested_time == "09:00"
        assert entry.flexibility == 0.5
        assert entry.priority == 3

    def test_to_dict(self):
        pattern = TemporalPattern(PatternType.DAILY, "test", 1.0, 0.8)
        entry = ScheduleEntry(pattern=pattern, suggested_time="10:00", flexibility=0.3)
        d = entry.to_dict()
        assert d["suggested_time"] == "10:00"
        assert d["pattern"] is not None


class TestDeadlineInfo:
    def test_default_creation(self):
        dl = DeadlineInfo(description="submit report")
        assert dl.description == "submit report"
        assert dl.urgency == 0.5
        assert dl.tasks_remaining == 0

    def test_to_dict(self):
        dl = DeadlineInfo(description="test", urgency=0.8, tasks_remaining=3)
        d = dl.to_dict()
        assert d["description"] == "test"
        assert d["urgency"] == 0.8

    def test_is_overdue(self):
        past = datetime.now() - timedelta(days=1)
        dl = DeadlineInfo(description="past", due_date=past)
        assert dl.is_overdue is True

    def test_not_overdue(self):
        future = datetime.now() + timedelta(days=7)
        dl = DeadlineInfo(description="future", due_date=future)
        assert dl.is_overdue is False

    def test_is_at_risk(self):
        dl = DeadlineInfo(description="urgent", urgency=0.9)
        assert dl.is_at_risk is True

    def test_not_at_risk(self):
        dl = DeadlineInfo(description="normal", urgency=0.3)
        assert dl.is_at_risk is False


class TestTemporalUnderstanding:
    @pytest.fixture
    def understanding(self):
        return TemporalUnderstanding()

    @pytest.fixture
    def sample_events(self):
        return [
            TemporalEvent(
                event_type=EventType.RECURRING,
                reference="every day",
                recurrence_pattern="daily",
                confidence=0.8,
            ),
            TemporalEvent(
                event_type=EventType.RECURRING,
                reference="every day",
                recurrence_pattern="daily",
                confidence=0.8,
            ),
            TemporalEvent(
                event_type=EventType.RECURRING,
                reference="every week",
                recurrence_pattern="weekly",
                confidence=0.7,
            ),
            TemporalEvent(
                event_type=EventType.DURATION,
                reference="30 minutes",
                duration_seconds=1800.0,
            ),
        ]

    def test_recognize_patterns(self, understanding, sample_events):
        patterns = understanding.recognize_patterns(sample_events)
        assert len(patterns) >= 2  # daily and weekly
        assert all(isinstance(p, TemporalPattern) for p in patterns)

    def test_daily_pattern_type(self, understanding, sample_events):
        patterns = understanding.recognize_patterns(sample_events)
        daily = [p for p in patterns if p.pattern_type == PatternType.DAILY]
        assert len(daily) >= 1
        assert daily[0].event_count >= 2

    def test_pattern_confidence(self, understanding, sample_events):
        patterns = understanding.recognize_patterns(sample_events)
        for p in patterns:
            assert 0.0 <= p.confidence <= 1.0

    def test_recognize_empty_events(self, understanding):
        patterns = understanding.recognize_patterns([])
        assert len(patterns) == 0

    def test_recognize_no_recurring(self, understanding):
        events = [
            TemporalEvent(EventType.DURATION, "30 min", duration_seconds=1800),
        ]
        patterns = understanding.recognize_patterns(events)
        assert len(patterns) == 0

    def test_infer_schedule(self, understanding, sample_events):
        patterns = understanding.recognize_patterns(sample_events)
        schedule = understanding.infer_schedule(patterns)
        assert len(schedule) >= 2
        assert all(isinstance(s, ScheduleEntry) for s in schedule)

    def test_infer_schedule_ordered_by_priority(self, understanding, sample_events):
        patterns = understanding.recognize_patterns(sample_events)
        schedule = understanding.infer_schedule(patterns)
        for i in range(len(schedule) - 1):
            assert schedule[i].priority >= schedule[i + 1].priority

    def test_infer_schedule_empty(self, understanding):
        schedule = understanding.infer_schedule([])
        assert len(schedule) == 0

    def test_track_deadline(self, understanding):
        future = datetime.now() + timedelta(days=3)
        understanding.track_deadline("report due", due_date=future, tasks_remaining=5, estimated_time=3600)
        deadlines = understanding.get_deadlines()
        assert len(deadlines) == 1
        assert deadlines[0].description == "report due"

    def test_track_overdue_deadline(self, understanding):
        past = datetime.now() - timedelta(days=1)
        understanding.track_deadline("overdue task", due_date=past)
        deadlines = understanding.get_deadlines()
        assert len(deadlines) == 1
        assert deadlines[0].is_overdue

    def test_get_at_risk_deadlines(self, understanding):
        near_future = datetime.now() + timedelta(hours=1)
        understanding.track_deadline("urgent", due_date=near_future, estimated_time=7200)
        understanding.track_deadline("normal", due_date=datetime.now() + timedelta(days=30))

        at_risk = understanding.get_at_risk_deadlines()
        assert len(at_risk) >= 1

    def test_get_statistics(self, understanding, sample_events):
        understanding.recognize_patterns(sample_events)
        understanding.track_deadline("test")
        stats = understanding.get_statistics()
        assert stats["patterns_recognized"] >= 2
        assert stats["deadlines_tracked"] >= 1

    def test_clear(self, understanding, sample_events):
        understanding.recognize_patterns(sample_events)
        understanding.track_deadline("test")
        understanding.clear()
        assert len(understanding.get_deadlines()) == 0


class TestPatternType:
    def test_enum_values(self):
        assert PatternType.DAILY.value == "daily"
        assert PatternType.WEEKLY.value == "weekly"
        assert PatternType.MONTHLY.value == "monthly"
        assert PatternType.SEASONAL.value == "seasonal"
        assert PatternType.CUSTOM.value == "custom"
