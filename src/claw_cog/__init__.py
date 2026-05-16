"""
claw-cog v1.5.0: AI Consciousness Component for Project Neo

A computational consciousness framework based on:
- Global Workspace Theory (GWT) - Baars, Dehaene
- C0-C1-C2 Layered Architecture - Dehaene et al.
- meta-d' Metacognitive Assessment - Maniscalco & Lau
- ITCMA: Integrated Temporal Consciousness Model Architecture (v1.5.0) - Husserl
- Five Theory Indicator Properties - Butlin et al.

Architecture:
    C2: Metacognitive (GoalTracking, Superego, Protention, TemporalPrediction)
    C1: Conscious Access (Global Workspace, Memory, Ego, TemporalUnderstanding)
    C0: Unconscious (Fast Patterns, Auto Responses, TemporalPerception)

Example:
    >>> from claw_cog import ConsciousAgent
    >>> agent = ConsciousAgent()
    >>> result = agent.process("Meeting every day for 2 hours")
    >>> print(result.output, result.confidence)
    >>> print(f"Events detected: {len(result.temporal_events)}")
    >>> print(f"Conflicts: {len(result.temporal_conflicts)}")
    >>> metrics = agent.assess_metacognition()
"""

from claw_cog.core.agent import (
    ConsciousAgent, ConsciousnessLevel, ProcessingResult,
    ConsciousnessResultWithTime,
)
from claw_cog.core.workspace import GlobalWorkspace
from claw_cog.core.layers import LayerManager
from claw_cog.config.defaults import Config
from claw_cog.exceptions import (
    ClawCogError,
    ConfigurationError,
    LayerError,
    WorkspaceError,
    AssessmentError,
)
# P1-1: Time Consciousness Enhancement (ITCMA)
from claw_cog.modules import (
    TemporalPerception, TemporalEvent, DurationEstimate, EventType,
    TemporalUnderstanding, TemporalPattern, ScheduleEntry, DeadlineInfo, PatternType,
    TemporalPrediction, PredictedEvent, TemporalConflict, ResolutionSuggestion, ConflictType,
)

__version__ = "1.5.0"
__all__ = [
    "ConsciousAgent",
    "ConsciousnessLevel",
    "ProcessingResult",
    "ConsciousnessResultWithTime",
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
]
