"""
LearningActionHandler — execute learning-related actions (feedback, update_policy).

Receives feedback signals and updates learning policies.
"""

from typing import Any, Dict
from datetime import datetime

from claw_cog.execution.context import Action, ExecutionContext
from claw_cog.execution.result import ActionResult
from claw_cog.execution.handlers.base import ActionHandler


class LearningActionHandler(ActionHandler):
    """Execute learning-related actions.

    Handles action types: feedback, update_policy.
    Stores feedback history for future policy improvements.
    """

    _LEARNING_TYPES = {"feedback", "update_policy"}

    def __init__(self):
        self._feedback_history: Dict[str, list] = {}
        self._policies: Dict[str, Dict[str, Any]] = {}

    def can_handle(self, action: Action) -> bool:
        return action.action_type in self._LEARNING_TYPES

    def execute(self, action: Action, context: ExecutionContext) -> ActionResult:
        method_map = {
            "feedback": self._process_feedback,
            "update_policy": self._process_update_policy,
        }
        handler = method_map.get(action.action_type)
        if handler is None:
            return ActionResult.failure_result(
                action.action_id,
                f"Unsupported learning action: {action.action_type}",
            )

        try:
            start = datetime.now()
            output = handler(action, context)
            duration = (datetime.now() - start).total_seconds() * 1000
            return ActionResult.success_result(
                action.action_id, output=output, duration_ms=duration
            )
        except Exception as e:
            return ActionResult.failure_result(action.action_id, error=str(e))

    def rollback(self, action: Action, rollback_data: Dict[str, Any]) -> bool:
        if action.action_type == "feedback":
            policy_key = action.parameters.get("policy_key", "")
            if policy_key in self._feedback_history and self._feedback_history[policy_key]:
                self._feedback_history[policy_key].pop()
            return True
        return True

    # ── Internal ────────────────────────────────────────────────────────────────

    def _process_feedback(self, action: Action, context: ExecutionContext) -> Dict[str, Any]:
        policy_key = action.parameters.get("policy_key", action.action_type)
        signal = action.parameters.get("signal", "neutral")
        confidence = action.parameters.get("confidence", 0.5)

        entry = {
            "signal": signal,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "description": action.description,
        }

        self._feedback_history.setdefault(policy_key, []).append(entry)
        return {"policy_key": policy_key, "status": "feedback_recorded", "entry": entry}

    def _process_update_policy(self, action: Action, context: ExecutionContext) -> Dict[str, Any]:
        policy_key = action.parameters.get("policy_key", "")
        new_policy = action.parameters.get("policy", {})

        old = self._policies.get(policy_key)
        self._policies[policy_key] = {
            "policy": new_policy,
            "updated_at": datetime.now().isoformat(),
        }
        return {
            "policy_key": policy_key,
            "status": "policy_updated",
            "previous": old,
        }

    def get_feedback(self, policy_key: str) -> list:
        """Get feedback history for a specific policy."""
        return self._feedback_history.get(policy_key, [])

    def get_policy(self, policy_key: str) -> Dict[str, Any]:
        """Get current policy for a key."""
        return self._policies.get(policy_key, {})
