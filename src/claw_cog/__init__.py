"""
claw-cog v3.1.0: AI Consciousness Component for Project Neo

A computational consciousness framework based on:
- Global Workspace Theory (GWT) - Baars, Dehaene
- C0-C1-C2 Layered Architecture - Dehaene et al.
- meta-d' Metacognitive Assessment - Maniscalco & Lau
- ITCMA: Integrated Temporal Consciousness Model Architecture (v2.0.0) - Husserl
- ETCLOVG: Extended Temporal Consciousness Layer with Observation, Volition, and Goal-tracking (v3.0.0)
- Five Theory Indicator Properties - Butlin et al.

Architecture:
    O: Observation (Anomaly Detection, Self Monitoring)
    V: Volition (Goal Tracking, Intention Selection)
    C2: Metacognitive (GoalTracking, Superego, Protention, TemporalPrediction)
    C1: Conscious Access (Global Workspace, Memory, Ego, TemporalUnderstanding)
    C0: Unconscious (Fast Patterns, Auto Responses, TemporalPerception)

Example:
    >>> from claw_cog import ConsciousAgent
    >>> agent = ConsciousAgent()
    >>> result = agent.process("Meeting every day for 2 hours")
    >>> print(result.output, result.confidence)
    >>> print(f"Goals: {len(result.goals)}")
    >>> print(f"Observations: {len(result.observations)}")
    >>> print(f"Anomalies: {len(result.anomalies)}")
    >>> metrics = agent.assess_metacognition()
"""

# Import modules first to avoid circular import with agent
from claw_cog.config.defaults import Config
from claw_cog.exceptions import (
    ClawCogError,
    ConfigurationError,
    LayerError,
    WorkspaceError,
    AssessmentError,
)
from claw_cog.core.workspace import GlobalWorkspace
from claw_cog.core.layers import LayerManager

# P1-1: Time Consciousness Enhancement (ITCMA)
from claw_cog.modules import (
    TemporalPerception, TemporalEvent, DurationEstimate, EventType,
    TemporalUnderstanding, TemporalPattern, ScheduleEntry, DeadlineInfo, PatternType,
    TemporalPrediction, PredictedEvent, TemporalConflict, ResolutionSuggestion, ConflictType,
)
# v1.8.0: Volition and Observation layers (ETCLOVG)
from claw_cog.modules import (
    VolitionEngine, Goal, GoalPriority, GoalStatus, Intention,
    GoalTracker, IntentionBuffer, IntentionConflict,
    ObservationEngine, Observation, Anomaly, SeverityLevel,
    SelfMonitor, AnomalyDetector,
)

from claw_cog.core.agent import (
    ConsciousAgent, ConsciousnessLevel, ProcessingResult,
    ConsciousnessResultWithTime, ConsciousnessResultWithVO,
)

# Execution Layer (v3.1.0)
from .execution import Action, ActionResult, ActionExecutor, ExecutionContext, RollbackManager
from .execution.handlers import (
    ActionHandler,
    MemoryActionHandler,
    LearningActionHandler,
    ExternalActionHandler,
)

__version__ = "3.1.0"
__all__ = [
    "ConsciousAgent",
    "ConsciousnessLevel",
    "ProcessingResult",
    "ConsciousnessResultWithTime",
    "ConsciousnessResultWithVO",
    "GlobalWorkspace",
    "LayerManager",
    "Config",
    "ClawCogError",
    "ConfigurationError",
    "LayerError",
    "WorkspaceError",
    "AssessmentError",
    # P1-1 Temporal Consciousness
    "TemporalPerception",
    "TemporalEvent",
    "DurationEstimate",
    "EventType",
    "TemporalUnderstanding",
    "TemporalPattern",
    "ScheduleEntry",
    "DeadlineInfo",
    "PatternType",
    "TemporalPrediction",
    "PredictedEvent",
    "TemporalConflict",
    "ResolutionSuggestion",
    "ConflictType",
    # v1.8.0: Volition
    "VolitionEngine",
    "Goal",
    "GoalPriority",
    "GoalStatus",
    "Intention",
    "GoalTracker",
    "IntentionBuffer",
    "IntentionConflict",
    # v1.8.0: Observation
    "ObservationEngine",
    "Observation",
    "Anomaly",
    "SeverityLevel",
    "SelfMonitor",
    "AnomalyDetector",
    # v3.1.0: Execution Layer
    "Action", "ActionResult", "ActionExecutor", "ExecutionContext", "RollbackManager",
    "ActionHandler", "MemoryActionHandler", "LearningActionHandler", "ExternalActionHandler",
]
