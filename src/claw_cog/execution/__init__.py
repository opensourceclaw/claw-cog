"""
claw-cog v3.1.0 — Execution Layer.

Action execution subsystem: dispatches cognitive decisions to
registered handlers, manages execution context and rollback.

Usage::

    from claw_cog.execution import ActionExecutor, Action, ExecutionContext, ActionResult

    executor = ActionExecutor()
    executor.register_handler("memory", MemoryActionHandler())
    result = executor.execute(Action(action_type="store_memory", ...), context)
"""

from .context import Action, ExecutionContext
from .result import ActionResult
from .rollback import RollbackManager
from .executor import ActionExecutor

__all__ = [
    "Action",
    "ActionExecutor",
    "ExecutionContext",
    "ActionResult",
    "RollbackManager",
]
