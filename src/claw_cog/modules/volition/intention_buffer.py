"""IntentionBuffer — stores intentions, detects conflicts, bounded capacity."""

from typing import List, Optional

from .types import GoalPriority, Intention, IntentionConflict


class IntentionBuffer:
    """A bounded-size buffer of intentions with conflict detection."""

    def __init__(self, max_size: int = 5):
        self.max_size = max_size
        self._buffer: List[Intention] = []
        self._stats = {"intentions_pushed": 0, "conflicts_detected": 0}

    def push(self, intention: Intention) -> Intention:
        """Push an intention onto the buffer. Evicts oldest if at capacity."""
        if len(self._buffer) >= self.max_size:
            self._buffer.pop(0)
        self._buffer.append(intention)
        self._stats["intentions_pushed"] += 1
        return intention

    def get_next(self) -> Optional[Intention]:
        """Get the highest-priority intention from the buffer."""
        if not self._buffer:
            return None
        order = {
            GoalPriority.CRITICAL: 0,
            GoalPriority.HIGH: 1,
            GoalPriority.MEDIUM: 2,
            GoalPriority.LOW: 3,
        }
        return max(self._buffer, key=lambda i: (3 - order.get(i.priority, 0), i.confidence))

    def detect_conflicts(self) -> List[IntentionConflict]:
        """Detect conflicts between intentions currently in the buffer."""
        conflicts = []
        for i in range(len(self._buffer)):
            for j in range(i + 1, len(self._buffer)):
                a, b = self._buffer[i], self._buffer[j]
                conflict = self._check_conflict(a, b)
                if conflict is not None:
                    conflicts.append(conflict)
                    self._stats["conflicts_detected"] += 1
        return conflicts

    def get_statistics(self) -> dict:
        return {**self._stats, "buffer_size": len(self._buffer)}

    def clear(self):
        """Clear the buffer and reset statistics."""
        self._buffer.clear()
        self._stats = {"intentions_pushed": 0, "conflicts_detected": 0}

    def _check_conflict(self, a: Intention, b: Intention) -> Optional[IntentionConflict]:
        """Check if two intentions conflict (resource, priority, or semantic)."""
        # Same goal_id means they're complementary, not conflicting
        if a.goal_id == b.goal_id:
            return None

        # Priority inversion: lower-priority intention has higher confidence
        prio_order = {
            GoalPriority.CRITICAL: 4,
            GoalPriority.HIGH: 3,
            GoalPriority.MEDIUM: 2,
            GoalPriority.LOW: 1,
        }
        a_prio = prio_order.get(a.priority, 0)
        b_prio = prio_order.get(b.priority, 0)

        if a_prio < b_prio and a.confidence > b.confidence:
            return IntentionConflict(
                intention1=a,
                intention2=b,
                conflict_type="priority_inversion",
                description=f"Lower priority intention '{a.action}' has higher confidence ({a.confidence}) than higher priority '{b.action}' ({b.confidence})",
                severity=0.5,
            )
        if b_prio < a_prio and b.confidence > a.confidence:
            return IntentionConflict(
                intention1=b,
                intention2=a,
                conflict_type="priority_inversion",
                description=f"Lower priority intention '{b.action}' has higher confidence ({b.confidence}) than higher priority '{a.action}' ({a.confidence})",
                severity=0.5,
            )
        return None


__all__ = ["IntentionBuffer"]
