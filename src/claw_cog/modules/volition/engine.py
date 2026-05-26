"""VolitionEngine — generates goals from C2 results and selects intentions."""

import uuid
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .types import Goal, GoalPriority, GoalStatus, Intention
from .goal_tracker import GoalTracker
from .intention_buffer import IntentionBuffer

logger = logging.getLogger(__name__)


class VolitionEngine:
    """
    Volition Engine — V layer of ETCLOVG architecture.

    Takes C2 metacognitive results and transforms them into:
    1. Goals (longer-term objectives)
    2. Intentions (concrete action decisions)

    Uses the ClawMemBridge to persist goals across sessions.
    """

    def __init__(
        self,
        goal_tracker: GoalTracker,
        intention_buffer: IntentionBuffer,
        memory=None,
    ):
        self.goal_tracker = goal_tracker
        self.intention_buffer = intention_buffer
        self.memory = memory
        self._stats = {"goals_generated": 0, "intentions_selected": 0}

    def generate_goals(
        self, c2_result, context: Optional[Dict[str, Any]] = None
    ) -> List[Goal]:
        """
        Generate goals from C2 metacognitive results.

        Mapping rules:
        - C2.recommendation -> Goal.description
        - C2.adjustment_type -> influences Goal.priority
        - C2.confidence_estimate -> stored in metadata
        - C2.performance_trend -> stored in metadata
        """
        goals = []
        if c2_result is None:
            return goals

        # Determine base priority from adjustment type and confidence
        priority = self._infer_priority(c2_result)
        now = datetime.now(timezone.utc).isoformat()

        # Main goal from C2 recommendation
        if c2_result.recommendation:
            goal = Goal(
                goal_id=f"goal-{uuid.uuid4().hex[:12]}",
                description=c2_result.recommendation,
                priority=priority,
                source="c2_recommendation",
                created_at=now,
                metadata={
                    "confidence_estimate": getattr(c2_result, "confidence_estimate", 0.5),
                    "performance_trend": getattr(c2_result, "performance_trend", "stable"),
                    "learning_signal": getattr(c2_result, "learning_signal", 0.0),
                },
            )
            goals.append(goal)

        # Additional goal if adjustment is needed
        if c2_result.needs_adjustment and c2_result.adjustment_type not in ("", "none"):
            adj_goal = Goal(
                goal_id=f"goal-{uuid.uuid4().hex[:12]}",
                description=f"Adjust processing: {c2_result.adjustment_type}",
                priority=GoalPriority.HIGH,
                source=f"c2_adjustment_{c2_result.adjustment_type}",
                created_at=now,
                metadata={"adjustment_type": c2_result.adjustment_type},
            )
            goals.append(adj_goal)

        # Store goals in tracker and memory bridge
        for goal in goals:
            self.goal_tracker.add(goal)
            if self.memory:
                try:
                    self.memory.store(
                        memory_type="goal",
                        content=f"Goal: {goal.description}",
                        metadata={
                            "goal_id": goal.goal_id,
                            "priority": goal.priority.value,
                            "status": goal.status.value,
                        },
                    )
                except Exception:
                    logger.debug("Failed to store goal in memory bridge", exc_info=True)

        self._stats["goals_generated"] += len(goals)
        return goals

    def select_intention(self, goals: List[Goal]) -> Optional[Intention]:
        """
        Select the highest-priority actionable intention from a list of goals.

        Each active goal produces one intention. The intention is pushed
        into the buffer and the highest-priority one is returned.
        """
        for goal in goals:
            if goal.status in (GoalStatus.PENDING, GoalStatus.ACTIVE):
                intention = Intention(
                    intention_id=f"int-{uuid.uuid4().hex[:12]}",
                    goal_id=goal.goal_id,
                    action=goal.description,
                    confidence=goal.metadata.get("confidence_estimate", 0.5),
                    priority=goal.priority,
                    created_at=datetime.now(timezone.utc).isoformat(),
                )
                self.intention_buffer.push(intention)

        active = self.intention_buffer.get_next()
        if active:
            self._stats["intentions_selected"] += 1
        return active

    def get_statistics(self) -> Dict[str, Any]:
        """Return engine statistics including tracker and buffer stats."""
        return {
            **self._stats,
            "tracker": self.goal_tracker.get_statistics(),
            "buffer": self.intention_buffer.get_statistics(),
        }

    def clear(self):
        """Clear all volition state."""
        self.goal_tracker.clear()
        self.intention_buffer.clear()
        self._stats = {"goals_generated": 0, "intentions_selected": 0}

    @staticmethod
    def _infer_priority(c2_result) -> GoalPriority:
        """Infer goal priority from C2 adjustment type and confidence."""
        adj_type = getattr(c2_result, "adjustment_type", "")
        conf = getattr(c2_result, "confidence_estimate", 0.5)

        if adj_type == "seek_help":
            return GoalPriority.CRITICAL
        if conf < 0.3:
            return GoalPriority.HIGH
        if conf < 0.5:
            return GoalPriority.MEDIUM
        return GoalPriority.LOW


__all__ = ["VolitionEngine"]
