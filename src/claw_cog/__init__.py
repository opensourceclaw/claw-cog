"""
claw-cog: AI Consciousness Component for Project Neo

A computational consciousness framework based on:
- Global Workspace Theory (GWT) - Baars, Dehaene
- C0-C1-C2 Layered Architecture - Dehaene et al.
- meta-d' Metacognitive Assessment - Maniscalco & Lau
- Five Theory Indicator Properties - Butlin et al.

Architecture:
    C2: Metacognitive Layer (GoalTracking, Superego, Protention)
    C1: Conscious Access Layer (Global Workspace, Memory, Ego)
    C0: Unconscious Layer (Fast Patterns, Auto Responses)

Example:
    >>> from claw_cog import ConsciousAgent
    >>> agent = ConsciousAgent()
    >>> result = agent.process("Hello, world!")
    >>> print(result.output, result.confidence)
    >>> metrics = agent.assess_metacognition()
    >>> print(f"meta-d': {metrics['meta_d_prime']:.3f}")
"""

from claw_cog.core.agent import ConsciousAgent, ConsciousnessLevel, ProcessingResult
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

__version__ = "1.0.0"
__all__ = [
    "ConsciousAgent",
    "ConsciousnessLevel",
    "ProcessingResult",
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
