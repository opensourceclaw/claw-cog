"""
ActionHandler — abstract base class for all action handlers.
"""

from abc import ABC, abstractmethod
from typing import Dict

from claw_cog.execution.context import Action, ExecutionContext
from claw_cog.execution.result import ActionResult


class ActionHandler(ABC):
    """Abstract base class for action handlers.

    Each handler specializes in executing a specific type of action
    and provides rollback capability.

    Usage::

        class MyHandler(ActionHandler):
            def can_handle(self, action: Action) -> bool:
                return action.action_type == "my_type"

            def execute(self, action: Action, context: ExecutionContext) -> ActionResult:
                return ActionResult.success_result(action.action_id)

            def rollback(self, action: Action, rollback_data: Dict) -> bool:
                return True
    """

    @abstractmethod
    def can_handle(self, action: Action) -> bool:
        """Determine whether this handler can execute the given action.

        Args:
            action: The action to check.

        Returns:
            True if this handler can process the action.
        """
        ...

    @abstractmethod
    def execute(self, action: Action, context: ExecutionContext) -> ActionResult:
        """Execute an action within the given context.

        Args:
            action: The action to execute.
            context: The current execution context.

        Returns:
            ActionResult with execution outcome.
        """
        ...

    @abstractmethod
    def rollback(self, action: Action, rollback_data: Dict) -> bool:
        """Roll back a previously executed action.

        Args:
            action: The action to roll back.
            rollback_data: Data saved before execution.

        Returns:
            True if rollback succeeded.
        """
        ...
