"""
Temporal Perception (C0 Enhancement — P1-1)

C0-level temporal detection: event recognition, duration estimation,
and sequence recognition from input streams.

Part of the ITCMA (Integrated Temporal Consciousness Model Architecture).
"""

import re
import math
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum


# ── Data Types ─────────────────────────────────────────────────────────────────

class EventType(Enum):
    """Types of temporal events."""
    INSTANTANEOUS = "instantaneous"  # Single moment (e.g., "now")
    DURATION = "duration"            # Time span (e.g., "2 hours")
    RECURRING = "recurring"          # Repeated (e.g., "every day")
    DEADLINE = "deadline"            # Future point (e.g., "by Friday")


@dataclass
class TemporalEvent:
    """A detected temporal event."""
    event_type: EventType
    reference: str             # Original text or timestamp
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    recurrence_pattern: Optional[str] = None  # "daily", "weekly", etc.
    confidence: float = 0.5

    def to_dict(self) -> dict:
        return {
            "event_type": self.event_type.value,
            "reference": self.reference,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "recurrence_pattern": self.recurrence_pattern,
            "confidence": self.confidence,
        }


@dataclass
class DurationEstimate:
    """Estimated duration for a task."""
    expected: float            # Expected duration in seconds
    confidence: float          # 0.0-1.0
    range_min: float = 0.0     # Lower bound
    range_max: float = 0.0     # Upper bound
    similar_task_count: int = 0

    def to_dict(self) -> dict:
        return {
            "expected_seconds": self.expected,
            "confidence": self.confidence,
            "range_min": self.range_min,
            "range_max": self.range_max,
            "similar_task_count": self.similar_task_count,
        }


# ── TemporalPerception ─────────────────────────────────────────────────────────

class TemporalPerception:
    """C0: Enhanced temporal perception.

    Detects temporal events from input text, estimates task durations,
    and recognizes time-based sequences.

    Usage:
        perception = TemporalPerception()
        events = perception.detect_events(["meeting at 3pm for 2 hours"])
        estimate = perception.estimate_duration({"type": "development"})
    """

    # Time expression patterns
    TIME_PATTERNS: List[Tuple[str, str, str]] = [
        # (regex, event_type, recurrence/format)
        # Duration expressions
        (r"(\d+)\s*(hours?|hrs?|小时|个小时)", "duration", "hours"),
        (r"(\d+)\s*(minutes?|mins?|分钟)", "duration", "minutes"),
        (r"(\d+)\s*(days?|天)", "duration", "days"),
        (r"(\d+)\s*(weeks?|周|星期)", "duration", "weeks"),

        # Recurring patterns
        (r"every\s+(day|morning|night|evening)", "recurring", "daily"),
        (r"每天|每日", "recurring", "daily"),
        (r"every\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", "recurring", "weekly"),
        (r"every\s+week", "recurring", "weekly"),
        (r"每周", "recurring", "weekly"),
        (r"every\s+month", "recurring", "monthly"),
        (r"每月", "recurring", "monthly"),

        # Deadline expressions
        (r"by\s+(tomorrow|next\s+\w+|monday|tuesday|friday)", "deadline", ""),
        (r"due\s+(tomorrow|next\s+\w+|today|tonight)", "deadline", ""),
        (r"(明天|后天|下周|下个月)之前", "deadline", ""),
        (r"deadline[:：]\s*(.+)", "deadline", ""),

        # Instantaneous
        (r"(now|right now|immediately|asap)", "instantaneous", ""),
        (r"(现在|马上|立刻|立即)", "instantaneous", ""),
    ]

    # Default duration estimates by task category (in seconds)
    DEFAULT_DURATIONS: Dict[str, float] = {
        "development": 7200.0,       # 2 hours
        "review": 1800.0,            # 30 minutes
        "testing": 3600.0,           # 1 hour
        "deployment": 900.0,         # 15 minutes
        "documentation": 1800.0,     # 30 minutes
        "meeting": 3600.0,           # 1 hour
        "analysis": 2700.0,          # 45 minutes
        "planning": 1800.0,          # 30 minutes
        "writing": 2700.0,           # 45 minutes
        "research": 5400.0,          # 1.5 hours
    }

    def __init__(self, memory=None):
        """Initialize temporal perception.

        Args:
            memory: Optional memory backend for historical data
        """
        self.memory = memory
        self._event_history: List[TemporalEvent] = []
        self._stats = {"events_detected": 0, "durations_estimated": 0}

    def detect_events(self, input_stream: List[str]) -> List[TemporalEvent]:
        """Detect temporal events from input text.

        Args:
            input_stream: List of text strings to analyze

        Returns:
            List of detected TemporalEvent objects
        """
        events = []

        for item in input_stream:
            if not item:
                continue

            for pattern, event_type, extra in self.TIME_PATTERNS:
                match = re.search(pattern, item, re.IGNORECASE)
                if match:
                    event = self._build_event(event_type, match, extra, item)
                    events.append(event)
                    self._event_history.append(event)
                    break  # One event per input item

        self._stats["events_detected"] += len(events)
        return events

    def estimate_duration(
        self, task: Dict, similar_tasks: Optional[List[Dict]] = None
    ) -> DurationEstimate:
        """Estimate task duration based on historical data.

        Args:
            task: Task dict with at least "type" key
            similar_tasks: Optional list of similar historical tasks with durations

        Returns:
            DurationEstimate with expected duration and confidence
        """
        self._stats["durations_estimated"] += 1

        task_type = task.get("type", "development")

        # Use similar tasks if available
        if similar_tasks and len(similar_tasks) > 0:
            durations = [t.get("duration", 0) for t in similar_tasks if t.get("duration")]
            if durations:
                avg = sum(durations) / len(durations)
                confidence = min(0.95, max(0.3, len(durations) / 10.0) + 0.05)
                return DurationEstimate(
                    expected=avg,
                    confidence=confidence,
                    range_min=avg * 0.7,
                    range_max=avg * 1.3,
                    similar_task_count=len(durations),
                )

        # Use default estimation
        default = self.DEFAULT_DURATIONS.get(task_type, 3600.0)
        return DurationEstimate(
            expected=default,
            confidence=0.3,
            range_min=default * 0.5,
            range_max=default * 2.0,
            similar_task_count=0,
        )

    def recognize_sequences(
        self, events: List[TemporalEvent]
    ) -> List[List[TemporalEvent]]:
        """Recognize time-based sequences from events.

        Groups events that have temporal ordering relationships.

        Args:
            events: List of temporal events

        Returns:
            List of event sequences (ordered lists)
        """
        if len(events) < 2:
            return [events] if events else []

        # Sort by start time if available
        timed_events = [e for e in events if e.start_time is not None]
        untimed_events = [e for e in events if e.start_time is None]

        sequences = []

        if timed_events:
            timed_events.sort(key=lambda e: e.start_time)
            sequences.append(timed_events)

        if untimed_events:
            sequences.append(untimed_events)

        return sequences

    def get_history(self, limit: int = 50) -> List[TemporalEvent]:
        """Get recent event history."""
        return self._event_history[-limit:]

    def get_statistics(self) -> Dict:
        """Get perception statistics."""
        return dict(self._stats)

    def clear_history(self):
        """Clear event history."""
        self._event_history.clear()

    # ── Private ────────────────────────────────────────────────────────────────

    @staticmethod
    def _build_event(
        event_type: str, match: re.Match, extra: str, original: str
    ) -> TemporalEvent:
        """Build a TemporalEvent from regex match."""
        now = datetime.now()

        event = TemporalEvent(
            event_type=EventType(event_type),
            reference=original,
            confidence=0.7,
        )

        if event_type == "duration":
            value = int(match.group(1))
            unit = match.group(2).lower()
            multipliers = {
                "hours": 3600, "hrs": 3600, "小时": 3600, "个小时": 3600,
                "minutes": 60, "mins": 60, "分钟": 60,
                "days": 86400, "天": 86400,
                "weeks": 604800, "周": 604800, "星期": 604800,
            }
            for key, mult in multipliers.items():
                if key in unit:
                    event.duration_seconds = value * mult
                    event.end_time = now + timedelta(seconds=event.duration_seconds)
                    break

        elif event_type == "recurring":
            event.recurrence_pattern = extra  # "daily", "weekly", etc.

        elif event_type == "instantaneous":
            event.start_time = now

        return event


__all__ = [
    'TemporalPerception',
    'TemporalEvent',
    'DurationEstimate',
    'EventType',
]
