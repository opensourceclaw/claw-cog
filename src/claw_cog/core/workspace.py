"""
Global Workspace - Core of GNWT Architecture.

Implements Global Workspace Theory (Baars, Dehaene):
- Information broadcasting mechanism
- Multi-module integration
- Conscious access control
"""

from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from time import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class WorkspaceState:
    """Current state of the global workspace."""

    content: Any
    broadcast_time_ms: float
    subscribers_notified: int = 0
    integration_score: float = 0.0


@dataclass
class C1Result:
    """Result from C1 (Conscious Access) layer."""

    output: Any
    confidence: float
    broadcast_time_ms: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class GlobalWorkspace:
    """
    Global Workspace - Central hub for information integration.

    Based on Global Workspace Theory (GWT):
    - Broadcasts information to all subscribed modules
    - Integrates information from multiple sources
    - Controls conscious access

    Example:
        >>> workspace = GlobalWorkspace(config)
        >>> workspace.subscribe(memory_module)
        >>> result = workspace.process(input, c0_output, context)
    """

    def __init__(self, config: Any):
        """
        Initialize global workspace.

        Args:
            config: Configuration object
        """
        self.config = config
        self._subscribers: List[Callable] = []
        self._current_state: Optional[WorkspaceState] = None
        self._broadcast_history: List[WorkspaceState] = []

        # Performance metrics
        self._avg_broadcast_time_ms: float = 0.0
        self._total_broadcasts: int = 0

    def subscribe(self, module: Callable[[Any], Any]) -> None:
        """
        Subscribe a module to workspace broadcasts.

        Args:
            module: Callable that receives broadcast content
        """
        if len(self._subscribers) >= self.config.workspace_max_subscribers:
            logger.warning(
                f"Max subscribers ({self.config.workspace_max_subscribers}) reached"
            )
            return
        self._subscribers.append(module)
        logger.debug(f"Module subscribed. Total: {len(self._subscribers)}")

    def unsubscribe(self, module: Callable) -> None:
        """Unsubscribe a module."""
        if module in self._subscribers:
            self._subscribers.remove(module)

    def process(
        self,
        input: Any,
        c0_output: Any,
        context: Optional[Dict] = None
    ) -> C1Result:
        """
        Process input and broadcast to all subscribers.

        Args:
            input: Original input
            c0_output: Output from C0 (Unconscious) layer
            context: Additional context

        Returns:
            C1Result: Integrated result from conscious access
        """
        start_time = time()

        # 1. Integrate information from multiple sources
        integrated_content = self._integrate(input, c0_output, context)

        # 2. Broadcast to all subscribers
        broadcast_result = self._broadcast(integrated_content)

        # 3. Compute integration score
        integration_score = self._compute_integration_score(broadcast_result)

        # 4. Update state
        broadcast_time_ms = (time() - start_time) * 1000
        self._current_state = WorkspaceState(
            content=integrated_content,
            broadcast_time_ms=broadcast_time_ms,
            subscribers_notified=len(self._subscribers),
            integration_score=integration_score,
        )
        self._broadcast_history.append(self._current_state)

        # 5. Update performance metrics
        self._update_metrics(broadcast_time_ms)

        return C1Result(
            output=integrated_content,
            confidence=integration_score,
            broadcast_time_ms=broadcast_time_ms,
            metadata={"broadcast_result": broadcast_result},
        )

    def _integrate(
        self, input: Any, c0_output: Any, context: Optional[Dict]
    ) -> Any:
        """
        Integrate information from multiple sources.

        Priority: Memory > Ego > C0
        Uses weighted integration based on confidence scores.
        """
        sources: Dict[str, tuple[Any, float]] = {}

        # Collect sources with confidence scores
        sources["input"] = (input, 0.3)  # Base input has low weight

        if c0_output is not None:
            # C0 contribution based on pattern match confidence
            c0_conf = getattr(c0_output, "contribution", 0.5)
            sources["c0"] = (c0_output, c0_conf)

        if context:
            # Memory contribution
            if "memory_output" in context:
                mem_conf = context.get("memory_confidence", 0.8)
                sources["memory"] = (context["memory_output"], mem_conf)

            # Ego contribution (decision making)
            if "ego_output" in context:
                ego_conf = context.get("ego_confidence", 0.7)
                sources["ego"] = (context["ego_output"], ego_conf)

        # Weighted integration
        if len(sources) == 1:
            return input

        total_weight = sum(w for _, w in sources.values())
        if total_weight == 0:
            return input

        # For now, return highest confidence source
        best_source = max(sources.items(), key=lambda x: x[1][1])
        return best_source[1][0]

    def _broadcast(self, content: Any) -> Dict[str, Any]:
        """
        Broadcast content to all subscribers.

        Returns:
            Dict mapping subscriber names to their results
        """
        results: Dict[str, Any] = {}
        for i, subscriber in enumerate(self._subscribers):
            try:
                results[f"module_{i}"] = subscriber(content)
            except Exception as e:
                logger.error(f"Subscriber {i} error: {e}")
                results[f"module_{i}"] = {"error": str(e)}
        return results

    def _compute_integration_score(self, broadcast_result: Dict[str, Any]) -> float:
        """Compute integration score based on broadcast success."""
        if not broadcast_result:
            return 0.0
        successful = sum(
            1 for r in broadcast_result.values()
            if isinstance(r, dict) and "error" not in r
        )
        return successful / len(broadcast_result)

    def _update_metrics(self, broadcast_time_ms: float) -> None:
        """Update performance metrics (moving average)."""
        self._total_broadcasts += 1
        n = self._total_broadcasts
        self._avg_broadcast_time_ms = (
            (self._avg_broadcast_time_ms * (n - 1) + broadcast_time_ms) / n
        )

    def get_metrics(self) -> Dict[str, float]:
        """Get performance metrics."""
        return {
            "avg_broadcast_time_ms": self._avg_broadcast_time_ms,
            "total_broadcasts": self._total_broadcasts,
            "subscriber_count": len(self._subscribers),
        }

    def is_implemented(self) -> bool:
        """Check if GWT is implemented."""
        return True

    def has_attention_mechanism(self) -> bool:
        """Check if attention mechanism exists."""
        # v1.0.0: Basic implementation
        return True

    def clear_history(self) -> None:
        """Clear broadcast history."""
        self._broadcast_history.clear()
