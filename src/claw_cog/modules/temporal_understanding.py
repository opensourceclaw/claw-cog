"""
Temporal Understanding (C1 Enhancement — P1-1)

C1-level temporal pattern recognition, schedule inference, and
deadline awareness. Builds on C0 TemporalPerception output.

Part of the ITCMA (Integrated Temporal Consciousness Model Architecture).
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


# ── Data Types ─────────────────────────────────────────────────────────────────

class PatternType(Enum):
    """Types of temporal patterns."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    SEASONAL = "seasonal"
    CUSTOM = "custom"


@dataclass
class TemporalPattern:
    """A recognized temporal pattern."""
    pattern_type: PatternType
    description: str
    frequency: float           # Occurrences per time unit
    confidence: float          # 0.0-1.0
    event_count: int = 0       # Number of observations
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    typical_duration: float = 0.0  # Typical duration in seconds
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "pattern_type": self.pattern_type.value,
            "description": self.description,
            "frequency": self.frequency,
            "confidence": self.confidence,
            "event_count": self.event_count,
            "first_seen": self.first_seen.isoformat() if self.first_seen else None,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "typical_duration": self.typical_duration,
            "metadata": self.metadata,
        }


@dataclass
class ScheduleEntry:
    """A single schedule entry."""
    pattern: TemporalPattern
    suggested_time: str        # e.g., "09:00", "Monday 10:00"
    flexibility: float         # 0.0-1.0 (1 = very flexible)
    priority: int = 3          # 1-5, higher = more important

    def to_dict(self) -> dict:
        return {
            "suggested_time": self.suggested_time,
            "flexibility": self.flexibility,
            "priority": self.priority,
            "pattern": self.pattern.to_dict() if self.pattern else None,
        }


@dataclass
class DeadlineInfo:
    """Information about a deadline."""
    description: str
    due_date: Optional[datetime] = None
    urgency: float = 0.5       # 0.0-1.0
    tasks_remaining: int = 0
    estimated_time_needed: float = 0.0  # seconds

    def to_dict(self) -> dict:
        return {
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "urgency": self.urgency,
            "tasks_remaining": self.tasks_remaining,
            "estimated_time_needed": self.estimated_time_needed,
        }

    @property
    def is_overdue(self) -> bool:
        if self.due_date:
            return datetime.now() > self.due_date
        return False

    @property
    def is_at_risk(self) -> bool:
        return self.urgency > 0.7


# ── TemporalUnderstanding ──────────────────────────────────────────────────────

class TemporalUnderstanding:
    """C1: Temporal pattern understanding and schedule inference.

    Analyzes collected events to recognize temporal patterns,
    infer optimal schedules, and track deadline awareness.

    Usage:
        understanding = TemporalUnderstanding()
        patterns = understanding.recognize_patterns(events)
        schedule = understanding.infer_schedule(patterns)
    """

    def __init__(self):
        self._event_store: List[Dict] = []
        self._pattern_library: Dict[str, TemporalPattern] = {}
        self._deadlines: List[DeadlineInfo] = []
        self._stats = {"patterns_recognized": 0, "schedules_inferred": 0}

    def recognize_patterns(
        self, events: List['TemporalEvent']
    ) -> List[TemporalPattern]:
        """Recognize temporal patterns from events.

        Analyzes recurring events to detect daily, weekly, monthly,
        and custom patterns.

        Args:
            events: List of TemporalEvent objects from C0

        Returns:
            List of recognized TemporalPattern objects
        """
        # Store events for learning
        for e in events:
            self._event_store.append(e.to_dict())

        # Group recurring events by their recurrence pattern
        recurring = [e for e in events if e.recurrence_pattern]
        patterns = []

        # Group by recurrence pattern
        by_pattern: Dict[str, List] = defaultdict(list)
        for e in recurring:
            by_pattern[e.recurrence_pattern].append(e)

        for pattern_key, event_group in by_pattern.items():
            pattern_type = self._classify_pattern(pattern_key)
            frequency = len(event_group) / max(len(events), 1)
            confidence = min(0.95, 0.5 + 0.2 * len(event_group))

            pattern = TemporalPattern(
                pattern_type=pattern_type,
                description=f"{pattern_key} recurring events ({len(event_group)} occurrences)",
                frequency=frequency,
                confidence=confidence,
                event_count=len(event_group),
                first_seen=event_group[0].start_time if event_group else None,
                last_seen=event_group[-1].start_time if event_group else None,
                typical_duration=sum(
                    e.duration_seconds or 0 for e in event_group
                ) / len(event_group) if event_group else 0,
            )

            patterns.append(pattern)
            self._pattern_library[pattern_key] = pattern

        self._stats["patterns_recognized"] += len(patterns)
        return patterns

    def infer_schedule(
        self, patterns: List[TemporalPattern]
    ) -> List[ScheduleEntry]:
        """Infer optimal schedule from recognized patterns.

        Args:
            patterns: List of recognized TemporalPattern objects

        Returns:
            List of ScheduleEntry suggestions
        """
        if not patterns:
            return []

        entries = []

        # Suggested times by pattern type
        default_times = {
            PatternType.DAILY: "09:00",
            PatternType.WEEKLY: "Monday 10:00",
            PatternType.MONTHLY: "1st of month 10:00",
            PatternType.SEASONAL: "start of season",
            PatternType.CUSTOM: "flexible",
        }

        for pattern in patterns:
            suggested_time = default_times.get(pattern.pattern_type, "flexible")

            # Priority based on confidence and frequency
            priority = self._compute_priority(pattern)

            entry = ScheduleEntry(
                pattern=pattern,
                suggested_time=suggested_time,
                flexibility=self._compute_flexibility(pattern),
                priority=priority,
            )
            entries.append(entry)

        # Sort by priority (highest first)
        entries.sort(key=lambda e: e.priority, reverse=True)

        self._stats["schedules_inferred"] += 1
        return entries

    def track_deadline(self, description: str, due_date: Optional[datetime] = None,
                        tasks_remaining: int = 0, estimated_time: float = 0.0):
        """Track a deadline with urgency awareness.

        Args:
            description: Deadline description
            due_date: When it's due
            tasks_remaining: Number of tasks left
            estimated_time: Estimated remaining time in seconds
        """
        urgency = self._compute_urgency(due_date, estimated_time)

        self._deadlines.append(DeadlineInfo(
            description=description,
            due_date=due_date,
            urgency=urgency,
            tasks_remaining=tasks_remaining,
            estimated_time_needed=estimated_time,
        ))

    def get_deadlines(self) -> List[DeadlineInfo]:
        """Get all tracked deadlines sorted by urgency."""
        return sorted(self._deadlines, key=lambda d: d.urgency, reverse=True)

    def get_at_risk_deadlines(self) -> List[DeadlineInfo]:
        """Get deadlines at risk (urgency > 0.7 or overdue)."""
        return [d for d in self._deadlines if d.is_at_risk or d.is_overdue]

    def get_statistics(self) -> Dict:
        """Get understanding statistics."""
        return {
            **self._stats,
            "stored_events": len(self._event_store),
            "deadlines_tracked": len(self._deadlines),
            "at_risk_deadlines": len(self.get_at_risk_deadlines()),
        }

    def clear(self):
        """Clear all stored data and reset statistics."""
        self._event_store.clear()
        self._pattern_library.clear()
        self._deadlines.clear()
        self._stats = {"patterns_recognized": 0, "schedules_inferred": 0}

    # ── Private ────────────────────────────────────────────────────────────────

    @staticmethod
    def _classify_pattern(pattern_key: str) -> PatternType:
        """Classify recurrence pattern type."""
        mapping = {
            "daily": PatternType.DAILY,
            "weekly": PatternType.WEEKLY,
            "monthly": PatternType.MONTHLY,
        }
        return mapping.get(pattern_key, PatternType.CUSTOM)

    @staticmethod
    def _compute_priority(pattern: TemporalPattern) -> int:
        """Compute priority (1-5) based on confidence and frequency."""
        score = int(pattern.confidence * 3 + pattern.frequency * 2)
        return max(1, min(5, score))

    @staticmethod
    def _compute_flexibility(pattern: TemporalPattern) -> float:
        """Compute schedule flexibility."""
        # Daily patterns are less flexible, custom more flexible
        flex_map = {
            PatternType.DAILY: 0.3,
            PatternType.WEEKLY: 0.5,
            PatternType.MONTHLY: 0.7,
            PatternType.SEASONAL: 0.8,
            PatternType.CUSTOM: 0.9,
        }
        return flex_map.get(pattern.pattern_type, 0.5)

    @staticmethod
    def _compute_urgency(
        due_date: Optional[datetime], estimated_time: float
    ) -> float:
        """Compute deadline urgency (0.0-1.0)."""
        if not due_date:
            return 0.5

        now = datetime.now()
        remaining = (due_date - now).total_seconds()

        if remaining <= 0:
            return 1.0  # Overdue

        if estimated_time <= 0:
            return 0.3

        # Urgency = time_needed / time_remaining
        ratio = estimated_time / max(remaining, 1)
        return min(1.0, ratio)


__all__ = [
    'TemporalUnderstanding',
    'TemporalPattern',
    'ScheduleEntry',
    'DeadlineInfo',
    'PatternType',
]
