"""
RollbackManager — manage action rollback data and execution.

Stores rollback snapshots and provides rollback capability
for actions that support it.
"""

from typing import Any, Dict, List, Optional


class RollbackManager:
    """Manage rollback data and execute rollbacks for failed actions.

    Stores rollback snapshots keyed by action_id and supports
    executing rollbacks in reverse execution order.

    Usage::

        rm = RollbackManager()
        rm.save_snapshot("action-1", {"backup": "original_data"})
        rm.rollback("action-1")  # Returns True
    """

    def __init__(self):
        self._snapshots: Dict[str, Dict[str, Any]] = {}
        self._rollback_log: List[Dict[str, Any]] = []

    def save_snapshot(self, action_id: str, data: Dict[str, Any]) -> None:
        """Save rollback data for an action.

        Overwrites any existing snapshot for the same action_id.
        """
        self._snapshots[action_id] = data

    def get_snapshot(self, action_id: str) -> Optional[Dict[str, Any]]:
        """Get rollback data for an action. Returns None if not found."""
        return self._snapshots.get(action_id)

    def has_snapshot(self, action_id: str) -> bool:
        """Check if an action has rollback data."""
        return action_id in self._snapshots

    def rollback(self, action_id: str) -> bool:
        """Execute rollback for an action.

        Returns True if rollback data existed and was removed.
        Returns False if no snapshot existed.
        """
        snapshot = self._snapshots.pop(action_id, None)
        if snapshot is None:
            return False
        self._rollback_log.append({
            "action_id": action_id,
            "snapshot": snapshot,
            "status": "rolled_back",
        })
        return True

    def rollback_all(self) -> int:
        """Rollback all saved snapshots in LIFO order.

        Returns:
            Number of actions rolled back.
        """
        count = 0
        for action_id in reversed(list(self._snapshots.keys())):
            self.rollback(action_id)
            count += 1
        return count

    def get_rollback_log(self) -> List[Dict[str, Any]]:
        """Get the rollback execution log."""
        return list(self._rollback_log)

    def reset(self) -> None:
        """Clear all snapshots and rollback log."""
        self._snapshots.clear()
        self._rollback_log.clear()

    @property
    def snapshot_count(self) -> int:
        """Number of stored rollback snapshots."""
        return len(self._snapshots)
