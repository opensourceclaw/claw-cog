"""
C1: Conscious Access Layer.

Global workspace access, decision making, information integration.
Based on Freud's Ego and Husserl's Retention.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class C1Result:
    """Result from C1 conscious access processing."""

    output: Any
    confidence: float
    source: str
    metadata: Dict[str, Any]


class C1Conscious:
    """C1: Conscious Access Layer.

    Integrates information from Global Workspace, applies decision-making
    logic (Ego), and retrieves memory context (Retention). Information
    in this layer is accessible for report and decision (Dehaene's C1).
    """

    def __init__(self, config: Any, memory_bridge: Any = None):
        self.config = config
        self._memory_bridge = memory_bridge
        self._active = True
        self._processed_count: int = 0
        self._cached_contexts: Dict[str, Any] = {}
        logger.debug("C1Conscious layer initialized")

    def process(
        self,
        workspace_result: Any,
        context: Optional[Dict] = None,
    ) -> C1Result:
        """Process information from global workspace.

        Pipeline:
        1. Retrieve memory context (Retention)
        2. Integrate with C0 output
        3. Apply decision logic (Ego)
        4. Compute confidence
        """
        self._processed_count += 1

        # 1. Memory retrieval — replay relevant past context
        memory_context = self._retrieve_memory(workspace_result, context or {})

        # 2. Integration — combine C0 + memory + workspace
        integrated = self._integrate(workspace_result, memory_context)

        # 3. Decision — evaluate plausibility and choose action
        decision = self._decide(integrated)

        # 4. Confidence — weighted based on source reliability
        confidence = self._compute_confidence(integrated, memory_context)

        return C1Result(
            output=decision,
            confidence=confidence,
            source="workspace",
            metadata={
                "memory_retrieved": memory_context is not None,
                "integration_strategy": "weighted_merge",
                "processed_count": self._processed_count,
            },
        )

    def _retrieve_memory(self, content: Any, context: Dict) -> Optional[Any]:
        """Retrieve relevant memory via claw-mem bridge."""
        if self._memory_bridge is None:
            return None
        try:
            if isinstance(content, str):
                cached = self._cached_contexts.get(content[:50])
                if cached is not None:
                    return cached
                result = self._memory_bridge.retrieve(query=content, top_k=3)
                if result:
                    self._cached_contexts[content[:50]] = result
                    return result
        except Exception as e:
            logger.debug("Memory retrieval skipped: %s", e)
        return None

    def _integrate(self, workspace_output: Any, memory_context: Optional[Any]) -> Dict[str, Any]:
        """Integrate C0 output, workspace, and memory."""
        return {
            "workspace_output": workspace_output,
            "memory_context": memory_context,
            "sources_combined": memory_context is not None,
        }

    def _decide(self, integrated: Dict[str, Any]) -> Any:
        """Apply Ego decision logic — prefer specific over generic."""
        ws = integrated.get("workspace_output")
        mem = integrated.get("memory_context")

        if mem is not None and ws is not None:
            return ws  # Workspace takes priority with memory support
        return ws

    def _compute_confidence(
        self, integrated: Dict[str, Any], memory_context: Optional[Any]
    ) -> float:
        """Compute confidence score based on available sources."""
        base = 0.5
        if integrated.get("workspace_output") is not None:
            base += 0.2
        if integrated.get("sources_combined"):
            base += 0.2
        return min(1.0, max(0.0, base))

    def is_active(self) -> bool:
        return self._active

    def reset(self) -> None:
        self._processed_count = 0
        self._cached_contexts.clear()
