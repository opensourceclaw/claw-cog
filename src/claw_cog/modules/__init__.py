"""Cognitive modules: Temporal, Memory, Ego, GoalTracking, FastPatterns.

P1-1: Temporal Consciousness Enhancement (ITCMA).
- TemporalPerception (C0): Event detection, duration estimation
- TemporalUnderstanding (C1): Pattern recognition, schedule inference
- TemporalPrediction (C2): Future prediction, conflict detection

v1.8.0: Volition and Observation layers (ETCLOVG).
- VolitionEngine (V): Goal generation, intention selection
- ObservationEngine (O): Layer state observation, anomaly detection
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

from .volition import (
    VolitionEngine, Goal, GoalPriority, GoalStatus, Intention,
    GoalTracker, IntentionBuffer, IntentionConflict,
)
from .observation import (
    ObservationEngine, Observation, Anomaly, SeverityLevel,
    SelfMonitor, AnomalyDetector,
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
    # v1.8.0: Volition
    'VolitionEngine',
    'Goal',
    'GoalPriority',
    'GoalStatus',
    'Intention',
    'GoalTracker',
    'IntentionBuffer',
    'IntentionConflict',
    # v1.8.0: Observation
    'ObservationEngine',
    'Observation',
    'Anomaly',
    'SeverityLevel',
    'SelfMonitor',
    'AnomalyDetector',
]
