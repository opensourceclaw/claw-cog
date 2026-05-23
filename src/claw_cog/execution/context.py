"""
ExecutionContext — execution context and trace management.

Each execution session creates a context that tracks actions,
supports nested child contexts, and provides trace history.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class Action:
    """An action to be executed by the execution layer.

    Attributes:
        action_id: Unique action identifier.
        action_type: Type of action (memory, learning, external).
        description: Human-readable description.
        parameters: Action parameters for the handler.
        source: Source of the action (volition, cognition, manual).
        priority: Execution priority (0=lowest, 10=highest).
        metadata: Additional contextual data.
    """

    action_id: str = field(default_factory=lambda: str(uuid4()))
    action_type: str = ""
    description: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    source: str = "volition"
    priority: int = 5
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "action_type": self.action_type,
            "description": self.description,
            "parameters": self.parameters,
            "source": self.source,
            "priority": self.priority,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Action":
        return cls(
            action_id=data.get("action_id", str(uuid4())),
            action_type=data.get("action_type", ""),
            description=data.get("description", ""),
            parameters=data.get("parameters", {}),
            source=data.get("source", "volition"),
            priority=data.get("priority", 5),
            metadata=data.get("metadata", {}),
        )


class ExecutionContext:
    """Execution context tracking actions and session state.

    Supports nested contexts for sub-executions and provides
    trace history for debugging and rollback.

    Usage::

        ctx = ExecutionContext()
        ctx.start_action(action)
        ctx.complete_action(action.action_id, success=True)
        trace = ctx.get_trace()
    """

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid4())
        self.timestamp = datetime.now()
        self.metadata: Dict[str, Any] = {}
        self.parent_context: Optional[ExecutionContext] = None
        self._actions: List[Action] = []
        self._completed: Dict[str, bool] = {}
        self._errors: Dict[str, str] = {}
        self._start_times: Dict[str, datetime] = {}
        self._children: List[ExecutionContext] = []

    def start_action(self, action: Action) -> None:
        """Record that an action has started execution."""
        self._actions.append(action)
        self._start_times[action.action_id] = datetime.now()

    def complete_action(self, action_id: str, success: bool, error: str = "") -> None:
        """Record action completion status."""
        self._completed[action_id] = success
        if error:
            self._errors[action_id] = error

    def get_action(self, action_id: str) -> Optional[Action]:
        """Get an action by ID."""
        for action in self._actions:
            if action.action_id == action_id:
                return action
        return None

    def get_trace(self) -> List[Action]:
        """Get the ordered list of actions in this context."""
        return list(self._actions)

    def get_errors(self) -> Dict[str, str]:
        """Get all recorded errors."""
        return dict(self._errors)

    def get_duration(self, action_id: str) -> Optional[float]:
        """Get execution duration in milliseconds for an action."""
        if action_id not in self._start_times:
            return None
        end = datetime.now()
        start = self._start_times[action_id]
        return (end - start).total_seconds() * 1000

    def create_child(self) -> "ExecutionContext":
        """Create a child execution context."""
        child = ExecutionContext()
        child.parent_context = self
        child.metadata["parent_session"] = self.session_id
        self._children.append(child)
        return child

    def get_all_actions(self) -> List[Action]:
        """Get all actions including those from child contexts."""
        actions = list(self._actions)
        for child in self._children:
            actions.extend(child.get_all_actions())
        return actions

    def reset(self) -> None:
        """Clear all tracking data."""
        self._actions.clear()
        self._completed.clear()
        self._errors.clear()
        self._start_times.clear()
        self._children.clear()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "actions": [a.to_dict() for a in self._actions],
            "completed": self._completed,
            "errors": self._errors,
        }
