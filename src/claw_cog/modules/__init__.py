"""Cognitive modules: Temporal, Memory, Ego, GoalTracking, FastPatterns.

P1-1: Temporal Consciousness Enhancement (ITCMA).
- TemporalPerception (C0): Event detection, duration estimation
- TemporalUnderstanding (C1): Pattern recognition, schedule inference
- TemporalPrediction (C2): Future prediction, conflict detection
"""

from .temporal_perception import (
    TemporalPerception, TemporalEvent, DurationEstimate, EventType,
)
from .temporal_understanding import (
    TemporalUnderstanding, TemporalPattern, ScheduleEntry, DeadlineInfo, PatternType,
)
from .temporal_prediction import (
    TemporalPrediction, PredictedEvent, TemporalConflict, ResolutionSuggestion, ConflictType,
)

__all__ = [
    'TemporalPerception',
    'TemporalEvent',
    'DurationEstimate',
    'EventType',
    'TemporalUnderstanding',
    'TemporalPattern',
    'ScheduleEntry',
    'DeadlineInfo',
    'PatternType',
    'TemporalPrediction',
    'PredictedEvent',
    'TemporalConflict',
    'ResolutionSuggestion',
    'ConflictType',
]
