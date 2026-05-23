"""GoalTracker — manages goal lifecycle: add, update, decompose, complete, abandon."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .types import Goal, GoalPriority, GoalStatus


class GoalTracker:
    """Tracks goals through their lifecycle with CRUD and decomposition support."""

    def __init__(self, max_goals: int = 10):
        self.max_goals = max_goals
        self._goals: Dict[str, Goal] = {}
        self._stats = {"goals_created": 0, "goals_completed": 0, "goals_abandoned": 0}

    def add(self, goal: Goal) -> Goal:
        """Add a new goal. If at capacity, abandon lowest-priority pending goal."""
        if len(self._goals) >= self.max_goals:
            self._evict_lowest_priority()
        self._goals[goal.goal_id] = goal
        self._stats["goals_created"] += 1
        return goal

    def update(
        self,
        goal_id: str,
        *,
        description: Optional[str] = None,
        priority: Optional[GoalPriority] = None,
        status: Optional[GoalStatus] = None,
        progress: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[Goal]:
        """Update fields on an existing goal. Returns updated goal or None."""
        goal = self._goals.get(goal_id)
        if goal is None:
            return None
        if description is not None:
            goal.description = description
        if priority is not None:
            goal.priority = priority
        if status is not None:
            prev = goal.status
            goal.status = status
            if status == GoalStatus.COMPLETED and prev != GoalStatus.COMPLETED:
                self._stats["goals_completed"] += 1
            elif status == GoalStatus.ABANDONED and prev != GoalStatus.ABANDONED:
                self._stats["goals_abandoned"] += 1
        if progress is not None:
            goal.progress = max(0.0, min(1.0, progress))
        if metadata is not None:
            goal.metadata.update(metadata)
        return goal

    def get_active(self) -> List[Goal]:
        """Return all goals that are PENDING or ACTIVE, sorted by priority."""
        order = {GoalPriority.CRITICAL: 0, GoalPriority.HIGH: 1, GoalPriority.MEDIUM: 2, GoalPriority.LOW: 3}
        active = [
            g for g in self._goals.values()
            if g.status in (GoalStatus.PENDING, GoalStatus.ACTIVE)
        ]
        active.sort(key=lambda g: order.get(g.priority, 99))
        return active

    def complete(self, goal_id: str) -> Optional[Goal]:
        """Mark a goal as completed."""
        return self.update(goal_id, status=GoalStatus.COMPLETED, progress=1.0)

    def abandon(self, goal_id: str) -> Optional[Goal]:
        """Abandon a goal."""
        return self.update(goal_id, status=GoalStatus.ABANDONED)

    def get(self, goal_id: str) -> Optional[Goal]:
        """Get a specific goal by ID."""
        return self._goals.get(goal_id)

    def get_all(self) -> List[Goal]:
        """Return all goals."""
        return list(self._goals.values())

    def get_statistics(self) -> Dict[str, Any]:
        """Return tracker statistics."""
        return {
            **self._stats,
            "active_count": len(self.get_active()),
            "total_count": len(self._goals),
        }

    def clear(self):
        """Clear all goals and reset statistics."""
        self._goals.clear()
        self._stats = {"goals_created": 0, "goals_completed": 0, "goals_abandoned": 0}

    @staticmethod
    def decompose(goal: Goal, sub_descriptions: List[str]) -> List[Goal]:
        """Decompose a goal into sub-goals sharing the same parent."""
        sub_goals = []
        for desc in sub_descriptions:
            sub = Goal(
                goal_id=str(uuid.uuid4()),
                description=desc,
                priority=goal.priority,
                source=goal.source,
                parent_goal_id=goal.goal_id,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            sub_goals.append(sub)
        return sub_goals

    def _evict_lowest_priority(self):
        """Remove the lowest-priority pending goal to make room."""
        order = {GoalPriority.CRITICAL: 4, GoalPriority.HIGH: 3, GoalPriority.MEDIUM: 2, GoalPriority.LOW: 1}
        pending = [
            (gid, g) for gid, g in self._goals.items()
            if g.status == GoalStatus.PENDING
        ]
        if not pending:
            active = [
                (gid, g) for gid, g in self._goals.items()
                if g.status == GoalStatus.ACTIVE
            ]
            pending = active
        if pending:
            lowest = min(pending, key=lambda x: order.get(x[1].priority, 0))
            self._goals[lowest[0]].status = GoalStatus.ABANDONED
            self._stats["goals_abandoned"] += 1


__all__ = ["GoalTracker"]
