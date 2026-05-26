"""
ConsciousAgent - Main entry point for claw-cog.

Provides unified interface for AI consciousness capabilities
based on GNWT and C0-C1-C2 architecture.

v1.5.0: Integrated Temporal Consciousness (ITCMA).
v1.8.0: Volition and Observation layers (ETCLOVG).
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging
from datetime import timedelta

from claw_cog.config.defaults import Config
from claw_cog.exceptions import ConfigurationError
from claw_cog.core.workspace import GlobalWorkspace, C1Result
from claw_cog.core.layers import LayerManager
from claw_cog.layers.c2_metacognitive import C2Result
from claw_cog.assessment.meta_d_prime import MetacognitiveAssessment

# P1-1 / v1.5.0: Temporal consciousness modules
from claw_cog.modules.temporal_perception import TemporalPerception, TemporalEvent
from claw_cog.modules.temporal_understanding import TemporalUnderstanding, TemporalPattern
from claw_cog.modules.temporal_prediction import TemporalPrediction, TemporalConflict, ResolutionSuggestion

# v1.8.0: Volition and Observation layers
from claw_cog.modules.volition.engine import VolitionEngine
from claw_cog.modules.volition.goal_tracker import GoalTracker
from claw_cog.modules.volition.intention_buffer import IntentionBuffer
from claw_cog.modules.volition.types import Goal, Intention
from claw_cog.modules.observation.engine import ObservationEngine
from claw_cog.modules.observation.self_monitor import SelfMonitor
from claw_cog.modules.observation.anomaly_detector import AnomalyDetector
from claw_cog.modules.observation.types import Observation, Anomaly

# Execution layer (v3.1.0)
from claw_cog.execution import Action, ActionExecutor, ExecutionContext
from claw_cog.execution.handlers import ActionHandler, MemoryActionHandler, LearningActionHandler

# Verification layer (v4.0.0)
from claw_cog.consciousness.verification import (
    VerificationOrchestrator,
    VerificationReport,
    OutputValidator,
    ConfidenceCalibrator,
    QualityAssessor,
    ConsistencyChecker,
)

logger = logging.getLogger(__name__)


class ConsciousnessLevel(Enum):
    """Consciousness level enumeration."""

    C0_UNCONSCIOUS = 0
    C1_CONSCIOUS_ACCESS = 1
    C2_METACOGNITIVE = 2


@dataclass
class ProcessingResult:
    """Result from conscious processing."""

    output: Any
    confidence: float
    level: ConsciousnessLevel
    metadata: Dict[str, Any]


@dataclass
class ConsciousnessResultWithTime(ProcessingResult):
    """
    v1.5.0: Processing result enriched with temporal consciousness data.

    Extends ProcessingResult with temporal events, patterns,
    predictions, and conflict analysis from ITCMA.
    """

    temporal_events: List[TemporalEvent] = field(default_factory=list)
    temporal_patterns: List[TemporalPattern] = field(default_factory=list)
    temporal_conflicts: List[TemporalConflict] = field(default_factory=list)
    resolution_suggestions: List[ResolutionSuggestion] = field(default_factory=list)
    deadline_alerts: List[str] = field(default_factory=list)


@dataclass
class ConsciousnessResultWithVO(ConsciousnessResultWithTime):
    """
    v1.8.0: Processing result enriched with Volition and Observation data.

    Extends ConsciousnessResultWithTime with goals, active intention,
    observations, and anomaly detection from the V/O layers (ETCLOVG).
    """

    goals: List[Goal] = field(default_factory=list)
    active_intention: Optional[Intention] = None
    observations: List[Observation] = field(default_factory=list)
    anomalies: List[Anomaly] = field(default_factory=list)


class ConsciousAgent:
    """
    Conscious Agent - AI consciousness component.

    Based on:
    - Global Workspace Theory (GWT) - Baars, Dehaene
    - C0-C1-C2 Layered Architecture - Dehaene et al.
    - meta-d' Metacognitive Assessment - Maniscalco & Lau

    Architecture:
        O: Observation (Anomaly Detection, Self Monitoring)
        V: Volition (Goal Tracking, Intention Selection)
        C2: Metacognitive (GoalTracking, Superego, Protention)
        C1: Conscious Access (Global Workspace, Memory, Ego)
        C0: Unconscious (Fast Patterns, Auto Responses)

    Example:
        >>> agent = ConsciousAgent()
        >>> result = agent.process("Hello, world!")
        >>> print(result.output, result.confidence)
        >>> metrics = agent.assess_metacognition()
    """

    def __init__(
        self,
        config: Optional[Config] = None,
        enable_c2: bool = True,
        memory_backend: str = "claw-mem",
    ):
        """
        Initialize conscious agent.

        Args:
            config: Configuration object
            enable_c2: Whether to enable C2 metacognitive layer
            memory_backend: Memory backend to use
        """
        self.config = config or Config()

        # Core components
        self.workspace = GlobalWorkspace(self.config)
        self.layers = LayerManager(self.config, enable_c2=enable_c2)
        self.assessment = MetacognitiveAssessment(self.config)

        # Memory bridge
        from claw_cog.integration.claw_mem_bridge import ClawMemBridge
        self.memory = ClawMemBridge(self.config)

        # v3.1.0: Execution layer
        self.executor: Optional[ActionExecutor] = None

        # v4.0.0: Verification layer (Consciousness)
        self._verifier = VerificationOrchestrator(
            validator=OutputValidator(),
            calibrator=ConfidenceCalibrator(
                ece_threshold=self.config.verification_calibration_ece_threshold,
                num_bins=self.config.verification_calibration_num_bins,
            ),
            quality_assessor=QualityAssessor(
                completeness_threshold=self.config.verification_quality_completeness_threshold,
                clarity_threshold=self.config.verification_quality_clarity_threshold,
                safety_threshold=self.config.verification_quality_safety_threshold,
                relevance_threshold=self.config.verification_quality_relevance_threshold,
            ),
            consistency_checker=ConsistencyChecker(
                deviation_threshold=self.config.verification_consistency_deviation_threshold,
            ),
        )

        # v1.5.0: Temporal consciousness modules (ITCMA)
        self._temporal_perception = TemporalPerception(memory=self.memory)
        self._temporal_understanding = TemporalUnderstanding()
        self._temporal_prediction = TemporalPrediction()

        # v1.8.0: Volition layer (V)
        self._goal_tracker = GoalTracker(max_goals=self.config.volition_max_goals)
        self._intention_buffer = IntentionBuffer(
            max_size=self.config.volition_intention_buffer_size
        )
        self._volition_engine = VolitionEngine(
            goal_tracker=self._goal_tracker,
            intention_buffer=self._intention_buffer,
            memory=self.memory,
        )

        # v1.8.0: Observation layer (O)
        self._self_monitor = SelfMonitor(
            history_size=self.config.observation_history_size
        )
        self._anomaly_detector = AnomalyDetector(
            low_threshold=self.config.observation_anomaly_low_threshold,
            medium_threshold=self.config.observation_anomaly_medium_threshold,
            high_threshold=self.config.observation_anomaly_high_threshold,
        )
        self._observation_engine = ObservationEngine(
            monitor=self._self_monitor,
            detector=self._anomaly_detector,
            memory=self.memory,
        )

        # State
        self._processing_history: List[ProcessingResult] = []

        logger.info(
            f"ConsciousAgent initialized: "
            f"C0 ✓, C1 ✓, C2 {'✓' if enable_c2 else '✗'}, "
            f"memory={memory_backend}, "
            f"temporal={self.config.temporal_enabled}, "
            f"volition={self.config.volition_enabled}, "
            f"observation={self.config.observation_enabled}"
        )

    def process(
        self,
        input: Any,
        context: Optional[Dict] = None,
        confidence_threshold: float = 0.7,
        enable_temporal: Optional[bool] = None,
        enable_vo: Optional[bool] = None,
    ) -> ProcessingResult:
        """
        Process input through consciousness layers.

        v1.5.0: Returns ConsciousnessResultWithTime when temporal is enabled.
        v1.8.0: Returns ConsciousnessResultWithVO when V/O is enabled.

        Args:
            input: Input data
            context: Optional context information
            confidence_threshold: Confidence threshold for decisions
            enable_temporal: Override config temporal_enabled setting
            enable_vo: Override config volition/observation enabled setting

        Returns:
            ProcessingResult, ConsciousnessResultWithTime, or ConsciousnessResultWithVO
        """
        if not 0.0 <= confidence_threshold <= 1.0:
            raise ConfigurationError(
                f"confidence_threshold must be 0.0–1.0, got {confidence_threshold}"
            )

        # Determine if temporal processing is active
        use_temporal = enable_temporal if enable_temporal is not None else self.config.temporal_enabled

        # Determine if V/O processing is active (v1.8.0)
        use_vo = enable_vo if enable_vo is not None else (
            self.config.volition_enabled or self.config.observation_enabled
        )

        # Prepare input text for temporal analysis
        if isinstance(input, str):
            input_text = input
        elif isinstance(input, list):
            input_text = " ".join(str(i) for i in input)
        else:
            input_text = str(input)

        # 0. Retrieve relevant memories for context
        memories = self.memory.retrieve_relevant(
            query=str(input),
            limit=5,
        )
        memory_context = self.memory.format_context(memories)

        if context is None:
            context = {}
        context["memory_output"] = memory_context
        context["memory_confidence"] = 0.8 if memories else 0.3

        # ── 1. C0 Temporal: Detect events from input ──────────────────────────
        temporal_events: List[TemporalEvent] = []
        if use_temporal:
            temporal_events = self._temporal_perception.detect_events(
                [input_text] if isinstance(input_text, str) else [input_text]
            )
            logger.debug(f"C0 Temporal: {len(temporal_events)} events detected")

        # 2. C0: Fast pattern matching (unconscious)
        c0_result = self.layers.c0.process(input, context)
        logger.debug(f"C0 processed: contribution={c0_result.contribution:.2f}")

        # 3. C1: Conscious access via global workspace
        c1_result = self.workspace.process(
            input=input,
            c0_output=c0_result.output,
            context=context,
        )
        logger.debug(f"C1 processed: confidence={c1_result.confidence:.2f}")

        # ── 4. C1 Temporal: Recognize patterns from events ────────────────────
        temporal_patterns: List[TemporalPattern] = []
        if use_temporal and temporal_events:
            temporal_patterns = self._temporal_understanding.recognize_patterns(
                temporal_events
            )
            logger.debug(f"C1 Temporal: {len(temporal_patterns)} patterns recognized")

        # 5. C2: Metacognitive monitoring (if enabled)
        c2_result: Optional[C2Result] = None
        if self.layers.c2_enabled and self.layers.c2:
            c2_result = self.layers.c2.monitor(
                c1_result=c1_result,
                confidence_threshold=confidence_threshold,
            )
            logger.debug(
                f"C2 monitored: needs_adjustment={c2_result.needs_adjustment}"
            )

            # Apply adjustments if needed
            if c2_result.needs_adjustment:
                c1_result = self._apply_c2_adjustment(c1_result, c2_result)

        # ── 6. C2 Temporal: Predict future events and detect conflicts ────────
        temporal_conflicts: List[TemporalConflict] = []
        resolution_suggestions: List[ResolutionSuggestion] = []
        deadline_alerts: List[str] = []
        if use_temporal and temporal_patterns:
            horizon = timedelta(days=self.config.temporal_horizon_days)
            predictions = self._temporal_prediction.predict_future_events(
                temporal_patterns, horizon=horizon
            )
            logger.debug(f"C2 Temporal: {len(predictions)} predictions made")

            temporal_conflicts = self._temporal_prediction.detect_conflicts(
                predictions
            )
            logger.debug(f"C2 Temporal: {len(temporal_conflicts)} conflicts detected")

            if temporal_conflicts:
                resolution_suggestions = self._temporal_prediction.suggest_resolution(
                    temporal_conflicts
                )
                # Build deadline alerts from high-severity conflicts
                for conflict in temporal_conflicts:
                    if conflict.severity == "high":
                        deadline_alerts.append(
                            f"[{conflict.conflict_type.value.upper()}] {conflict.description}"
                        )

        # ── 7. V: Volition — Generate goals and select intention ───────────────
        goals: List[Goal] = []
        active_intention: Optional[Intention] = None
        if use_vo and self.config.volition_enabled:
            goals = self._volition_engine.generate_goals(
                c2_result=c2_result,
                context=context,
            )
            logger.debug(f"V: {len(goals)} goals generated")

            if goals:
                active_intention = self._volition_engine.select_intention(goals)
                logger.debug(
                    f"V: active intention={'selected' if active_intention else 'none'}"
                )

        # ── 8. O: Observation — Observe layer states and detect anomalies ──────
        observations: List[Observation] = []
        anomalies: List[Anomaly] = []
        if use_vo and self.config.observation_enabled:
            layer_states = {
                "c0": {"confidence": c0_result.contribution},
                "c1": {"confidence": c1_result.confidence},
                "c2": {
                    "confidence_estimate": c2_result.confidence_estimate if c2_result else 0.5,
                    "learning_signal": c2_result.learning_signal if c2_result else 0.0,
                    "attention_score": c2_result.attention_score if c2_result else 0.5,
                },
                "memory": {
                    "context_confidence": context.get("memory_confidence", 0.3),
                },
                "volition": {
                    "active_goal_count": len(self._goal_tracker.get_active()),
                    "buffer_size": len(self._intention_buffer._buffer),
                },
            }
            observations = self._observation_engine.observe(layer_states)
            logger.debug(f"O: {len(observations)} observations made")

            if observations:
                anomalies = self._observation_engine.detect_anomalies(observations)
                logger.debug(f"O: {len(anomalies)} anomalies detected")

        # 9. Build final result
        if use_vo:
            result = ConsciousnessResultWithVO(
                output=c1_result.output,
                confidence=c1_result.confidence,
                level=self._determine_level(c1_result),
                metadata={
                    "c0_contribution": c0_result.contribution,
                    "c0_pattern": c0_result.pattern_matched,
                    "c2_monitoring": c2_result.__dict__ if c2_result else None,
                    "broadcast_time_ms": c1_result.broadcast_time_ms,
                    "temporal_events_count": len(temporal_events),
                    "temporal_patterns_count": len(temporal_patterns),
                    "temporal_conflicts_count": len(temporal_conflicts),
                    "vo_goals_count": len(goals),
                    "vo_observations_count": len(observations),
                    "vo_anomalies_count": len(anomalies),
                },
                temporal_events=temporal_events,
                temporal_patterns=temporal_patterns,
                temporal_conflicts=temporal_conflicts,
                resolution_suggestions=resolution_suggestions,
                deadline_alerts=deadline_alerts,
                goals=goals,
                active_intention=active_intention,
                observations=observations,
                anomalies=anomalies,
            )
        elif use_temporal:
            result = ConsciousnessResultWithTime(
                output=c1_result.output,
                confidence=c1_result.confidence,
                level=self._determine_level(c1_result),
                metadata={
                    "c0_contribution": c0_result.contribution,
                    "c0_pattern": c0_result.pattern_matched,
                    "c2_monitoring": c2_result.__dict__ if c2_result else None,
                    "broadcast_time_ms": c1_result.broadcast_time_ms,
                    "temporal_events_count": len(temporal_events),
                    "temporal_patterns_count": len(temporal_patterns),
                    "temporal_conflicts_count": len(temporal_conflicts),
                },
                temporal_events=temporal_events,
                temporal_patterns=temporal_patterns,
                temporal_conflicts=temporal_conflicts,
                resolution_suggestions=resolution_suggestions,
                deadline_alerts=deadline_alerts,
            )
        else:
            result = ProcessingResult(
                output=c1_result.output,
                confidence=c1_result.confidence,
                level=self._determine_level(c1_result),
                metadata={
                    "c0_contribution": c0_result.contribution,
                    "c0_pattern": c0_result.pattern_matched,
                    "c2_monitoring": c2_result.__dict__ if c2_result else None,
                    "broadcast_time_ms": c1_result.broadcast_time_ms,
                },
            )

        # 10. Record history for metacognitive assessment
        self._processing_history.append(result)
        if len(self._processing_history) > self.config.assessment_history_size:
            self._processing_history.pop(0)

        # 11. Store reflection if C2 monitoring indicates learning
        if c2_result and c2_result.needs_adjustment:
            self.memory.store(
                memory_type="reflection",
                content=f"Adjustment needed: {c2_result.adjustment_type}",
                metadata={"confidence": c1_result.confidence},
            )

        # ── 9.5. V: Verification — Validate, calibrate, assess quality and consistency ─
        if self.config.verification_enabled:
            verification_report = self._verifier.verify(
                result,
                history=self._processing_history,
                context={},
            )
            result.metadata["verification"] = verification_report.to_dict()
            logger.debug(
                f"V: verification {'passed' if verification_report.passed else 'failed'}"
            )

        # 12. Store temporal events as memories (v1.5.0)
        if use_temporal and temporal_events:
            for event in temporal_events[:5]:  # Store top 5 events
                self.memory.store(
                    memory_type="experience",
                    content=f"Temporal event: {event.event_type.value} - {event.reference}",
                    metadata={
                        "event_type": event.event_type.value,
                        "confidence": event.confidence,
                        "temporal": True,
                    },
                )

        return result

    def _apply_c2_adjustment(
        self, c1_result: C1Result, c2_result: C2Result
    ) -> C1Result:
        """Apply C2 adjustment to C1 result."""
        # TODO: Implement actual adjustment logic
        # v1.0.0: Basic adjustment
        if c2_result.adjustment_type == "confidence":
            # Increase confidence threshold
            return C1Result(
                output=c1_result.output,
                confidence=min(c1_result.confidence * 1.1, 1.0),
                broadcast_time_ms=c1_result.broadcast_time_ms,
                metadata=c1_result.metadata,
            )
        return c1_result

    def _determine_level(self, c1_result: C1Result) -> ConsciousnessLevel:
        """Determine consciousness level of result."""
        if c1_result.confidence > 0.8:
            return ConsciousnessLevel.C2_METACOGNITIVE
        elif c1_result.confidence > 0.5:
            return ConsciousnessLevel.C1_CONSCIOUS_ACCESS
        else:
            return ConsciousnessLevel.C0_UNCONSCIOUS

    def enable_execution(self, handlers: Optional[List[ActionHandler]] = None,
                         config: Any = None) -> ActionExecutor:
        """Enable the execution layer for this agent.

        Creates an ActionExecutor and registers the provided handlers.
        If no handlers are provided, registers Memory and Learning handlers.

        Args:
            handlers: Optional list of ActionHandler instances.
            config: Optional config for the ActionExecutor.

        Returns:
            The created ActionExecutor.
        """
        self.executor = ActionExecutor(config=config)

        if handlers:
            for handler in handlers:
                self.executor.register_handler(handler.__class__.__name__, handler)
        else:
            # Register default handlers
            self.executor.register_handler("memory_handler", MemoryActionHandler())
            self.executor.register_handler("learning_handler", LearningActionHandler())

        return self.executor

    @property
    def verifier(self) -> VerificationOrchestrator:
        """The verification orchestrator for this agent."""
        return self._verifier

    def verify(self, result: Any,
               history: Optional[List[Any]] = None) -> VerificationReport:
        """Run verification on a processing result.

        Args:
            result: The processing result to verify.
            history: Optional list of previous results for consistency checking.

        Returns:
            VerificationReport with overall passed/failed and sub-results.
        """
        if history is None:
            history = self._processing_history[:-1] if len(self._processing_history) > 1 else []
        return self._verifier.verify(result, history=history, context={})

    def process_and_execute(self, input: Any,
                            context: Optional[Dict] = None,
                            confidence_threshold: float = 0.7) -> Any:
        """Process input and execute any resulting actions.

        Args:
            input: The input to process.
            context: Optional context dictionary.
            confidence_threshold: Confidence threshold for processing.

        Returns:
            The processing result with execution_results attached.
        """
        result = self.process(input, context=context,
                              confidence_threshold=confidence_threshold)

        if self.executor is None:
            return result

        # Extract actions from VO result if available
        actions = self._extract_actions(result)
        if actions:
            exec_ctx = ExecutionContext()
            execution_results = self.executor.execute_batch(actions, context=exec_ctx)

            # Attach execution results to the processing result
            if hasattr(result, 'execution_results'):
                result.execution_results = execution_results
            else:
                # Dynamically add if attribute doesn't exist
                setattr(result, 'execution_results', execution_results)

        return result

    def _extract_actions(self, result: Any) -> List[Action]:
        """Extract actions from a processing result.

        Converts Volition intentions to executable actions.
        """
        actions = []

        # Check for VO results (ConsciousnessResultWithVO)
        if hasattr(result, 'active_intention') and result.active_intention:
            intention = result.active_intention
            actions.append(Action(
                action_type="learning",
                description=f"Execute intention: {intention.action}",
                parameters={
                    "intention_id": intention.intention_id,
                    "goal_id": intention.goal_id,
                    "confidence": intention.confidence,
                },
                source="volition",
            ))

        # Check for anomalies
        if hasattr(result, 'anomalies') and result.anomalies:
            for anomaly in result.anomalies[:3]:  # Limit to top 3
                actions.append(Action(
                    action_type="notification",
                    description=f"Anomaly: {anomaly.description}",
                    parameters={
                        "anomaly_id": anomaly.anomaly_id,
                        "severity": anomaly.severity,
                        "message": anomaly.description,
                    },
                    source="observation",
                ))

        return actions

    def assess_metacognition(self) -> Dict[str, float]:
        """
        Assess metacognitive capabilities.

        Returns:
            Dict containing meta-d', d', M-ratio, etc.
        """
        return self.assessment.compute_metrics(self._processing_history)

    def get_indicator_properties(self) -> Dict[str, Any]:
        """
        Get indicator properties with detailed coverage scores.

        Returns:
            Dict mapping theory names to boolean or sub-property dict
        """
        return {
            "GWT": self.workspace.is_implemented(),
            "RPT": {
                "recurrent_processing": True,
                "feedback_loops": self.layers.has_feedback_loops(),
                "temporal_integration": self.config.temporal_enabled,
                "hierarchical_processing": True,
            },
            "HOT": {
                "higher_order_representation": self.layers.c2_enabled,
                "meta_monitoring": self.layers.c2_enabled,
                "self_awareness": self.layers.c2_enabled,
                "introspection": self.layers.c2_enabled,
            },
            "PP": self.config.temporal_enabled,  # v1.5.0: Predictive Processing via temporal
            "ETCLOVG": {
                "volition": self.config.volition_enabled,
                "observation": self.config.observation_enabled,
                "temporal": self.config.temporal_enabled,
            },
            "AST": {
                "attention_schema": self.workspace.has_attention_mechanism(),
                "precision_weighting": True,
                "resource_allocation": True,
            },
        }

    def get_indicator_scores(self) -> Dict[str, float]:
        """Get indicator properties as coverage percentages (rc.2)."""
        props = self.get_indicator_properties()
        scores = {}
        for theory, value in props.items():
            if isinstance(value, dict):
                true_count = sum(1 for v in value.values() if v)
                total = len(value)
                scores[theory] = true_count / total if total > 0 else 0.0
            else:
                scores[theory] = 1.0 if value else 0.0
        return scores

    def get_metrics(self) -> Dict[str, Any]:
        """Get all performance metrics including temporal, volition, and observation stats."""
        metrics = {
            "workspace": self.workspace.get_metrics(),
            "layers": self.layers.get_layer_status(),
            "history_size": len(self._processing_history),
        }
        if self.config.temporal_enabled:
            metrics["temporal"] = {
                "perception": self._temporal_perception.get_statistics(),
                "understanding": self._temporal_understanding.get_statistics(),
                "prediction": self._temporal_prediction.get_statistics(),
            }
        if self.config.volition_enabled:
            metrics["volition"] = self._volition_engine.get_statistics()
        if self.config.observation_enabled:
            metrics["observation"] = self._observation_engine.get_statistics()
        return metrics

    def generate_calibration_data(self, n_samples: int = 20) -> None:
        """Generate calibration data for meta-d' calculation.

        Injects synthetic ProcessingResult entries with varying confidences
        to bootstrap the metacognitive assessment. Uses both high-confidence
        (correct) and low-confidence (incorrect) trials.
        """
        import random
        random.seed(42)

        for i in range(n_samples):
            # Generate varying confidence: mix of high (correct) and low (incorrect)
            is_correct = i % 3 != 0  # ~67% correct
            if is_correct:
                confidence = random.uniform(0.6, 0.95)
            else:
                confidence = random.uniform(0.1, 0.45)

            result = ProcessingResult(
                output=f"calibration_{i}",
                confidence=confidence,
                level=self._determine_level_from_confidence(confidence),
                metadata={"calibration": True},
            )
            self._processing_history.append(result)

        # Trim to history limit
        while len(self._processing_history) > self.config.assessment_history_size:
            self._processing_history.pop(0)

    def _determine_level_from_confidence(
        self, confidence: float
    ) -> "ConsciousnessLevel":
        """Determine consciousness level from a confidence value."""
        if confidence > 0.8:
            return ConsciousnessLevel.C2_METACOGNITIVE
        elif confidence > 0.5:
            return ConsciousnessLevel.C1_CONSCIOUS_ACCESS
        return ConsciousnessLevel.C0_UNCONSCIOUS

    def reset(self) -> None:
        """Reset agent state including temporal, volition, observation, and verification modules."""
        self._processing_history.clear()
        self.layers.reset()
        self.workspace.clear_history()
        self._temporal_perception.clear_history()
        self._temporal_understanding.clear()
        self._temporal_prediction.clear()
        self._volition_engine.clear()
        self._observation_engine.clear()
        self._verifier.reset()
