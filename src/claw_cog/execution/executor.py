"""
ActionExecutor — dispatches actions to registered handlers.

Manages handler registration, action execution (single and batch),
and rollback for failed actions.
"""

import time
from typing import Any, Dict, List, Optional

from claw_cog.execution.context import Action, ExecutionContext
from claw_cog.execution.result import ActionResult
from claw_cog.execution.rollback import RollbackManager
from claw_cog.execution.handlers.base import ActionHandler


class ActionExecutor:
    """Execute cognitive decisions as concrete actions.

    Registers ActionHandler instances for different action types
    and dispatches actions to the appropriate handler.

    Usage::

        executor = ActionExecutor()
        executor.register_handler("memory", MemoryActionHandler())
        result = executor.execute(action, context)
    """

    def __init__(self, config: Optional[Any] = None):
        self._config = config
        self._handlers: Dict[str, ActionHandler] = {}
        self._context: Optional[ExecutionContext] = None
        self._rollback_manager = RollbackManager()

    @property
    def context(self) -> Optional[ExecutionContext]:
        return self._context

    @property
    def rollback_manager(self) -> RollbackManager:
        return self._rollback_manager

    def register_handler(self, action_type: str, handler: ActionHandler) -> None:
        """Register a handler for a specific action type.

        Args:
            action_type: Action type string this handler handles.
            handler: The ActionHandler implementation.

        Raises:
            ValueError: If the action_type is already registered.
        """
        self._handlers[action_type] = handler

    def unregister_handler(self, action_type: str) -> bool:
        """Unregister a handler. Returns False if not found."""
        if action_type in self._handlers:
            del self._handlers[action_type]
            return True
        return False

    def get_handler(self, action_type: str) -> Optional[ActionHandler]:
        """Get handler for an action type. Returns None if not registered."""
        return self._handlers.get(action_type)

    def execute(self, action: Action, context: Optional[ExecutionContext] = None) -> ActionResult:
        """Execute a single action.

        Finds the appropriate handler, executes with context,
        and saves rollback data.

        Args:
            action: The action to execute.
            context: Optional execution context. Creates one if None.

        Returns:
            ActionResult with execution outcome.
        """
        ctx = context or self._context or ExecutionContext()

        # Find handler
        handler = self._find_handler(action)
        if handler is None:
            return ActionResult.failure_result(
                action.action_id,
                f"No handler registered for action type: {action.action_type}",
            )

        # Start tracking
        ctx.start_action(action)
        start = time.perf_counter()

        # Execute
        result = handler.execute(action, ctx)
        result.duration_ms = (time.perf_counter() - start) * 1000

        # Save rollback data if available
        if result.rollback_data:
            self._rollback_manager.save_snapshot(action.action_id, result.rollback_data)

        # Record completion
        ctx.complete_action(action.action_id, result.success, result.error or "")
        return result

    def execute_batch(
        self, actions: List[Action], context: Optional[ExecutionContext] = None
    ) -> List[ActionResult]:
        """Execute multiple actions sequentially.

        On failure, attempts rollback for previously executed actions
        in reverse order.

        Args:
            actions: List of actions to execute.
            context: Optional execution context.

        Returns:
            List of ActionResult in execution order.
        """
        ctx = context or self._context or ExecutionContext()
        results: List[ActionResult] = []

        for action in actions:
            result = self.execute(action, context=ctx)
            results.append(result)

            if not result.success:
                # Rollback previously successful actions in reverse
                self._rollback_previous(results, actions)
                break

        return results

    def rollback(self, action: Action) -> bool:
        """Rollback a specific action using its handler.

        Args:
            action: The action to rollback.

        Returns:
            True if rollback succeeded.
        """
        handler = self._find_handler(action)
        if handler is None:
            return False

        snapshot = self._rollback_manager.get_snapshot(action.action_id)
        if snapshot is None:
            return False

        return handler.rollback(action, snapshot)

    def rollback_all(self) -> int:
        """Rollback all actions with saved snapshots.

        Returns:
            Number of actions rolled back.
        """
        return self._rollback_manager.rollback_all()

    def list_handlers(self) -> List[str]:
        """List all registered action types."""
        return list(self._handlers.keys())

    def reset(self) -> None:
        """Clear handlers, context and rollback data."""
        self._handlers.clear()
        self._context = None
        self._rollback_manager.reset()

    # ── Internal ────────────────────────────────────────────────────────────────

    def _find_handler(self, action: Action) -> Optional[ActionHandler]:
        """Find a handler that can execute the given action."""
        # Direct type match first
        handler = self._handlers.get(action.action_type)
        if handler:
            return handler

        # Fallback: check can_handle
        for h in self._handlers.values():
            if h.can_handle(action):
                return h

        return None

    def _rollback_previous(self, results: List[ActionResult], actions: List[Action]) -> None:
        """Rollback previously successful actions in reverse order."""
        for i in range(len(results) - 2, -1, -1):
            if results[i].success:
                action = actions[i]
                handler = self._find_handler(action)
                if handler:
                    snapshot = self._rollback_manager.get_snapshot(action.action_id)
                    if snapshot:
                        handler.rollback(action, snapshot)
