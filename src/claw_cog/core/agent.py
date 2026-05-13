"""
ConsciousAgent - Main entry point for claw-cog.

Provides unified interface for AI consciousness capabilities
based on GNWT and C0-C1-C2 architecture.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

from claw_cog.config.defaults import Config
from claw_cog.exceptions import ConfigurationError
from claw_cog.core.workspace import GlobalWorkspace, C1Result
from claw_cog.core.layers import LayerManager
from claw_cog.layers.c0_unconscious import C0Result
from claw_cog.layers.c2_metacognitive import C2Result
from claw_cog.assessment.meta_d_prime import MetacognitiveAssessment

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


class ConsciousAgent:
    """
    Conscious Agent - AI consciousness component.

    Based on:
    - Global Workspace Theory (GWT) - Baars, Dehaene
    - C0-C1-C2 Layered Architecture - Dehaene et al.
    - meta-d' Metacognitive Assessment - Maniscalco & Lau

    Architecture:
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

        # State
        self._processing_history: List[ProcessingResult] = []

        logger.info(
            f"ConsciousAgent initialized: "
            f"C0 ✓, C1 ✓, C2 {'✓' if enable_c2 else '✗'}, "
            f"memory={memory_backend}"
        )

    def process(
        self,
        input: Any,
        context: Optional[Dict] = None,
        confidence_threshold: float = 0.7,
    ) -> ProcessingResult:
        """
        Process input through consciousness layers.

        Args:
            input: Input data
            context: Optional context information
            confidence_threshold: Confidence threshold for decisions

        Returns:
            ProcessingResult: Processing result with confidence and level
        """
        if not 0.0 <= confidence_threshold <= 1.0:
            raise ConfigurationError(
                f"confidence_threshold must be 0.0–1.0, got {confidence_threshold}"
            )

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

        # 1. C0: Fast pattern matching (unconscious)
        c0_result = self.layers.c0.process(input, context)
        logger.debug(f"C0 processed: contribution={c0_result.contribution:.2f}")

        # 2. C1: Conscious access via global workspace
        c1_result = self.workspace.process(
            input=input,
            c0_output=c0_result.output,
            context=context,
        )
        logger.debug(f"C1 processed: confidence={c1_result.confidence:.2f}")

        # 3. C2: Metacognitive monitoring (if enabled)
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

        # 4. Build final result
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

        # 5. Record history for metacognitive assessment
        self._processing_history.append(result)
        if len(self._processing_history) > self.config.assessment_history_size:
            self._processing_history.pop(0)
        
        # 6. Store reflection if C2 monitoring indicates learning
        if c2_result and c2_result.needs_adjustment:
            self.memory.store(
                memory_type="reflection",
                content=f"Adjustment needed: {c2_result.adjustment_type}",
                metadata={"confidence": c1_result.confidence},
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

    def assess_metacognition(self) -> Dict[str, float]:
        """
        Assess metacognitive capabilities.

        Returns:
            Dict containing meta-d', d', M-ratio, etc.
        """
        return self.assessment.compute_metrics(self._processing_history)

    def get_indicator_properties(self) -> Dict[str, bool]:
        """
        Get indicator properties coverage.

        Returns:
            Dict mapping theory names to coverage status
        """
        return {
            "GWT": self.workspace.is_implemented(),
            "RPT": self.layers.has_feedback_loops(),
            "HOT": self.layers.c2_enabled,
            "PP": False,  # v2.0.0
            "AST": self.workspace.has_attention_mechanism(),
        }

    def get_metrics(self) -> Dict[str, Any]:
        """Get all performance metrics."""
        return {
            "workspace": self.workspace.get_metrics(),
            "layers": self.layers.get_layer_status(),
            "history_size": len(self._processing_history),
        }

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
        """Reset agent state."""
        self._processing_history.clear()
        self.layers.reset()
        self.workspace.clear_history()
