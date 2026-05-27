"""
MemoryActionHandler — execute memory-related actions (store, retrieve, update, delete).

Integrates with claw-mem via ClawMemBridge.
"""

from typing import Any, Dict
from datetime import datetime

from claw_cog.execution.context import Action, ExecutionContext
from claw_cog.execution.result import ActionResult
from claw_cog.execution.handlers.base import ActionHandler


class MemoryActionHandler(ActionHandler):
    """Execute memory-related actions.

    Handles action types: store_memory, retrieve_memory, update_memory, delete_memory.
    Falls back gracefully when claw-mem is not available.
    """

    _MEMORY_TYPES = {"memory", "store_memory", "retrieve_memory", "update_memory", "delete_memory"}

    def __init__(self, memory_bridge: Any = None):
        """Initialize with optional ClawMemBridge.

        Args:
            memory_bridge: Optional ClawMemBridge instance for memory operations.
        """
        self._bridge = memory_bridge
        self._store: Dict[str, Dict[str, Any]] = {}  # In-memory fallback

    def can_handle(self, action: Action) -> bool:
        return action.action_type in self._MEMORY_TYPES

    def execute(self, action: Action, context: ExecutionContext) -> ActionResult:
        method_map = {
            "memory": self._store_memory,  # Generic → store
            "store_memory": self._store_memory,
            "retrieve_memory": self._retrieve_memory,
            "update_memory": self._update_memory,
            "delete_memory": self._delete_memory,
        }
        handler = method_map.get(action.action_type)
        if handler is None:
            return ActionResult.failure_result(
                action.action_id,
                f"Unsupported memory action: {action.action_type}",
            )

        try:
            start = datetime.now()
            output = handler(action, context)
            duration = (datetime.now() - start).total_seconds() * 1000
            result = ActionResult.success_result(
                action.action_id, output=output, duration_ms=duration
            )
            # Attach rollback data for store operations
            if action.action_type in ("memory", "store_memory") and "previous" in output:
                result.rollback_data = {"previous": output["previous"]}
            return result
        except Exception as e:
            return ActionResult.failure_result(action.action_id, error=str(e))

    def rollback(self, action: Action, rollback_data: Dict[str, Any]) -> bool:
        if action.action_type == "store_memory":
            key = action.parameters.get("key", "")
            if rollback_data.get("previous") is None:
                self._store.pop(key, None)
            else:
                self._store[key] = rollback_data["previous"]
            return True
        return True  # Other operations are read-only or idempotent

    # ── Internal ────────────────────────────────────────────────────────────────

    def _store_memory(self, action: Action, context: ExecutionContext) -> Dict[str, Any]:
        key = action.parameters.get("key", action.action_id)
        content = action.parameters.get("content", action.description)
        memory_type = action.parameters.get("memory_type", "episodic")

        previous = self._store.get(key)
        self._store[key] = {
            "content": content,
            "memory_type": memory_type,
            "stored_at": datetime.now().isoformat(),
        }

        if self._bridge:
            try:
                self._bridge.store(content=content, memory_type=memory_type, key=key)
            except Exception:
                pass  # Fall back to in-memory

        return {"key": key, "status": "stored", "previous": previous}

    def _retrieve_memory(self, action: Action, context: ExecutionContext) -> Dict[str, Any]:
        key = action.parameters.get("key", "")
        entry = self._store.get(key)
        if entry:
            return {"key": key, "found": True, "content": entry["content"]}

        if self._bridge:
            try:
                result = self._bridge.retrieve(key=key)
                if result:
                    return {"key": key, "found": True, "content": result}
            except Exception:
                pass

        return {"key": key, "found": False, "content": None}

    def _update_memory(self, action: Action, context: ExecutionContext) -> Dict[str, Any]:
        key = action.parameters.get("key", "")
        content = action.parameters.get("content", "")
        if key in self._store:
            self._store[key]["content"] = content
            self._store[key]["updated_at"] = datetime.now().isoformat()
            return {"key": key, "status": "updated"}
        return {"key": key, "status": "not_found"}

    def _delete_memory(self, action: Action, context: ExecutionContext) -> Dict[str, Any]:
        key = action.parameters.get("key", "")
        if key in self._store:
            del self._store[key]
            return {"key": key, "status": "deleted"}
        return {"key": key, "status": "not_found"}
