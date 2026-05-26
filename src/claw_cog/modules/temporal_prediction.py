"""
Temporal Prediction (C2 Enhancement — P1-1)

C2-level future event prediction, conflict detection, and
resolution suggestion. Uses patterns from C1 to predict and plan.

Part of the ITCMA (Integrated Temporal Consciousness Model Architecture).
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum


# ── Data Types ─────────────────────────────────────────────────────────────────

class ConflictType(Enum):
    """Types of temporal conflicts."""
    OVERLAP = "overlap"       # Two events at overlapping times
    RESOURCE = "resource"     # Insufficient resources
    DEADLINE = "deadline"     # Cannot meet deadline


@dataclass
class PredictedEvent:
    """A predicted future event."""
    description: str
    predicted_time: datetime
    duration_seconds: float = 0.0
    confidence: float = 0.5
    resource_need: float = 1.0    # 0.0-1.0 normalized resource requirement
    source_pattern: Optional['TemporalPattern'] = None

    def to_dict(self) -> dict:
        return {
            "description": self.description,
            "predicted_time": self.predicted_time.isoformat() if self.predicted_time else None,
            "duration_seconds": self.duration_seconds,
            "confidence": self.confidence,
            "resource_need": self.resource_need,
        }


@dataclass
class TemporalConflict:
    """A detected temporal conflict."""
    conflict_type: ConflictType
    description: str
    events: List[PredictedEvent] = field(default_factory=list)
    severity: str = "medium"   # low / medium / high
    suggested_resolution: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "conflict_type": self.conflict_type.value,
            "description": self.description,
            "severity": self.severity,
            "suggested_resolution": self.suggested_resolution,
            "events": [e.to_dict() for e in self.events],
        }


@dataclass
class ResolutionSuggestion:
    """A suggestion for resolving a temporal conflict."""
    conflict: TemporalConflict
    strategy: str             # "reschedule", "allocate", "escalate"
    alternatives: List[dict] = field(default_factory=list)
    details: str = ""
    feasibility: float = 0.5  # 0.0-1.0

    def to_dict(self) -> dict:
        return {
            "strategy": self.strategy,
            "alternatives": self.alternatives,
            "details": self.details,
            "feasibility": self.feasibility,
            "conflict": self.conflict.to_dict(),
        }


# ── TemporalPrediction ─────────────────────────────────────────────────────────

class TemporalPrediction:
    """C2: Temporal prediction and conflict detection.

    Uses recognized patterns to predict future events, detect
    scheduling conflicts, and suggest resolutions.

    Usage:
        prediction = TemporalPrediction()
        events = prediction.predict_future_events(patterns, horizon_days=7)
        conflicts = prediction.detect_conflicts(events, schedule)
        resolutions = prediction.suggest_resolution(conflicts)
    """

    # Default resource capacities
    DEFAULT_RESOURCE_CAPACITY: float = 1.0

    def __init__(self):
        self.resource_capacity = self.DEFAULT_RESOURCE_CAPACITY
        self._prediction_history: List[PredictedEvent] = []
        self._conflict_history: List[TemporalConflict] = []
        self._stats = {
            "predictions_made": 0,
            "conflicts_detected": 0,
            "resolutions_suggested": 0,
        }

    def predict_future_events(
        self,
        patterns: List['TemporalPattern'],
        horizon: Optional[timedelta] = None,
    ) -> List[PredictedEvent]:
        """Predict future events within the given horizon.

        Args:
            patterns: Recognized temporal patterns from C1
            horizon: Time window for predictions (default: 7 days)

        Returns:
            List of PredictedEvent objects
        """
        if horizon is None:
            horizon = timedelta(days=7)

        now = datetime.now()
        horizon_end = now + horizon
        predictions = []

        for pattern in patterns:
            next_times = self._predict_next_occurrences(
                pattern, now, horizon_end
            )

            for pred_time in next_times:
                event = PredictedEvent(
                    description=pattern.description,
                    predicted_time=pred_time,
                    duration_seconds=pattern.typical_duration,
                    confidence=pattern.confidence,
                    resource_need=self._estimate_resource_need(pattern),
                    source_pattern=pattern,
                )
                predictions.append(event)

        self._stats["predictions_made"] += len(predictions)
        self._prediction_history.extend(predictions)

        return sorted(predictions, key=lambda p: p.predicted_time)

    def detect_conflicts(
        self,
        predictions: List[PredictedEvent],
        existing_schedule: Optional[List['ScheduleEntry']] = None,
    ) -> List[TemporalConflict]:
        """Detect temporal conflicts among predictions.

        Checks for:
        - Overlapping events
        - Resource over-allocation
        - Deadline violations

        Args:
            predictions: Predicted future events
            existing_schedule: Optional existing schedule entries

        Returns:
            List of TemporalConflict objects
        """
        conflicts = []

        # Sort by predicted time
        sorted_events = sorted(predictions, key=lambda p: p.predicted_time)

        # Check for overlaps
        for i in range(len(sorted_events)):
            for j in range(i + 1, len(sorted_events)):
                e1 = sorted_events[i]
                e2 = sorted_events[j]

                if self._check_overlap(e1, e2):
                    severity = "high" if e1.confidence > 0.7 and e2.confidence > 0.7 else "medium"

                    conflicts.append(TemporalConflict(
                        conflict_type=ConflictType.OVERLAP,
                        description=f"Overlap: '{e1.description}' and '{e2.description}'",
                        events=[e1, e2],
                        severity=severity,
                    ))

        # Check for resource over-allocation
        resource_conflicts = self._check_resource_conflicts(sorted_events)
        conflicts.extend(resource_conflicts)

        # Check for deadline pressure
        deadline_conflicts = self._check_deadline_conflicts(sorted_events)
        conflicts.extend(deadline_conflicts)

        self._stats["conflicts_detected"] += len(conflicts)
        self._conflict_history.extend(conflicts)

        return conflicts

    def suggest_resolution(
        self, conflicts: List[TemporalConflict]
    ) -> List[ResolutionSuggestion]:
        """Suggest resolution strategies for conflicts.

        Args:
            conflicts: Detected temporal conflicts

        Returns:
            List of ResolutionSuggestion objects
        """
        suggestions = []

        for conflict in conflicts:
            if conflict.conflict_type == ConflictType.OVERLAP:
                suggestion = self._suggest_overlap_resolution(conflict)
            elif conflict.conflict_type == ConflictType.RESOURCE:
                suggestion = self._suggest_resource_resolution(conflict)
            elif conflict.conflict_type == ConflictType.DEADLINE:
                suggestion = self._suggest_deadline_resolution(conflict)
            else:
                suggestion = ResolutionSuggestion(
                    conflict=conflict,
                    strategy="escalate",
                    details="Manual review required",
                    feasibility=0.3,
                )

            suggestions.append(suggestion)

        self._stats["resolutions_suggested"] += len(suggestions)
        return suggestions

    def get_statistics(self) -> Dict:
        """Get prediction statistics."""
        return dict(self._stats)

    def clear(self):
        """Clear prediction history and stats."""
        self._prediction_history.clear()
        self._conflict_history.clear()
        self._stats = {
            "predictions_made": 0,
            "conflicts_detected": 0,
            "resolutions_suggested": 0,
        }

    # ── Private ────────────────────────────────────────────────────────────────

    @staticmethod
    def _predict_next_occurrences(
        pattern: 'TemporalPattern',
        start: datetime,
        horizon: datetime,
    ) -> List[datetime]:
        """Predict next occurrences of a pattern."""
        if not pattern or pattern.event_count < 1:
            return []

        occurrences = []
        current = start

        # Determine step based on pattern type
        if pattern.pattern_type.value == "daily":
            step = timedelta(days=1)
        elif pattern.pattern_type.value == "weekly":
            step = timedelta(weeks=1)
        elif pattern.pattern_type.value == "monthly":
            step = timedelta(days=30)
        elif pattern.pattern_type.value == "seasonal":
            step = timedelta(days=90)
        else:
            step = timedelta(days=7)  # Default custom: weekly

        # Generate occurrences until horizon
        max_occurrences = 20
        while current < horizon and len(occurrences) < max_occurrences:
            current += step
            if current <= horizon:
                occurrences.append(current)

        return occurrences

    @staticmethod
    def _estimate_resource_need(pattern: 'TemporalPattern') -> float:
        """Estimate resource needed for a pattern-based event."""
        if pattern.event_count < 3:
            return 0.5
        # More frequent = more resource need
        return min(1.0, 0.3 + 0.2 * pattern.frequency)

    @staticmethod
    def _check_overlap(e1: PredictedEvent, e2: PredictedEvent) -> bool:
        """Check if two predicted events overlap in time."""
        if e1.predicted_time is None or e2.predicted_time is None:
            return False

        e1_start = e1.predicted_time
        e1_end = e1_start + timedelta(seconds=e1.duration_seconds)
        e2_start = e2.predicted_time
        e2_end = e2_start + timedelta(seconds=e2.duration_seconds)

        # Overlap if intervals intersect
        return e1_start < e2_end and e2_start < e1_end

    def _check_resource_conflicts(
        self, events: List[PredictedEvent]
    ) -> List[TemporalConflict]:
        """Check for resource over-allocation in a time window."""
        conflicts = []

        # Simple check: total resource need in a 1-hour window
        now = datetime.now()
        window_end = now + timedelta(hours=1)
        window_events = [
            e for e in events
            if e.predicted_time and now <= e.predicted_time < window_end
        ]

        total_resource = sum(e.resource_need for e in window_events)
        if total_resource > self.resource_capacity * 1.2:
            conflicts.append(TemporalConflict(
                conflict_type=ConflictType.RESOURCE,
                description=f"Resource over-allocation ({total_resource:.1f} > {self.resource_capacity})",
                events=window_events,
                severity="medium" if total_resource < self.resource_capacity * 1.5 else "high",
            ))

        return conflicts

    @staticmethod
    def _check_deadline_conflicts(
        events: List[PredictedEvent]
    ) -> List[TemporalConflict]:
        """Check for deadline pressure conflicts."""
        conflicts = []

        now = datetime.now()
        # Events predicted too close to each other with high resource needs
        for e in events:
            if not e.predicted_time:
                continue
            remaining = (e.predicted_time - now).total_seconds()
            if remaining <= 0:
                continue

            required = e.duration_seconds
            if required > 0 and remaining < required * 1.5:
                conflicts.append(TemporalConflict(
                    conflict_type=ConflictType.DEADLINE,
                    description=f"Deadline risk: insufficient time for '{e.description}'",
                    events=[e],
                    severity="high",
                ))

        return conflicts

    @staticmethod
    def _suggest_overlap_resolution(
        conflict: TemporalConflict
    ) -> ResolutionSuggestion:
        """Suggest resolution for overlapping events."""
        alternatives = []
        if len(conflict.events) >= 2:
            # Suggest moving later event back
            later = max(conflict.events, key=lambda e: e.predicted_time)
            later_time = later.predicted_time + timedelta(hours=1)
            alternatives.append({
                "action": "reschedule",
                "event": later.description,
                "suggested_time": later_time.isoformat(),
            })

        return ResolutionSuggestion(
            conflict=conflict,
            strategy="reschedule",
            alternatives=alternatives,
            details="Consider rescheduling one of the overlapping events to avoid conflicts.",
            feasibility=0.8,
        )

    @staticmethod
    def _suggest_resource_resolution(
        conflict: TemporalConflict
    ) -> ResolutionSuggestion:
        """Suggest resolution for resource conflicts."""
        return ResolutionSuggestion(
            conflict=conflict,
            strategy="allocate",
            alternatives=[{"action": "prioritize", "details": "Focus on highest-priority events first"}],
            details="Prioritize events and defer lower-priority ones to avoid resource contention.",
            feasibility=0.6,
        )

    @staticmethod
    def _suggest_deadline_resolution(
        conflict: TemporalConflict
    ) -> ResolutionSuggestion:
        """Suggest resolution for deadline conflicts."""
        return ResolutionSuggestion(
            conflict=conflict,
            strategy="escalate",
            alternatives=[
                {"action": "reduce_scope", "details": "Reduce scope to meet deadline"},
                {"action": "extend_deadline", "details": "Request deadline extension"},
                {"action": "add_resources", "details": "Add more resources"},
            ],
            details="Deadline at risk. Consider reducing scope, extending the deadline, or adding resources.",
            feasibility=0.5,
        )


__all__ = [
    'TemporalPrediction',
    'PredictedEvent',
    'TemporalConflict',
    'ResolutionSuggestion',
    'ConflictType',
]
