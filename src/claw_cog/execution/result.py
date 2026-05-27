"""
ActionResult — standardized execution result with rollback support.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ActionResult:
    """Standardized result from executing an action.

    Attributes:
        action_id: The action this result corresponds to.
        success: Whether execution succeeded.
        output: Result output data.
        error: Error message if failed.
        duration_ms: Execution duration in milliseconds.
        rollback_data: Data needed for rollback if supported.
    """

    action_id: str = ""
    success: bool = False
    output: Optional[Any] = None
    error: Optional[str] = None
    duration_ms: float = 0.0
    rollback_data: Optional[Dict[str, Any]] = field(default=None)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "rollback_data": self.rollback_data,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ActionResult":
        return cls(
            action_id=data.get("action_id", ""),
            success=data.get("success", False),
            output=data.get("output"),
            error=data.get("error"),
            duration_ms=data.get("duration_ms", 0.0),
            rollback_data=data.get("rollback_data"),
        )

    @staticmethod
    def success_result(
        action_id: str, output: Any = None, duration_ms: float = 0.0
    ) -> "ActionResult":
        """Factory for successful results."""
        return ActionResult(
            action_id=action_id,
            success=True,
            output=output,
            duration_ms=duration_ms,
        )

    @staticmethod
    def failure_result(action_id: str, error: str = "", duration_ms: float = 0.0) -> "ActionResult":
        """Factory for failed results."""
        return ActionResult(
            action_id=action_id,
            success=False,
            error=error,
            duration_ms=duration_ms,
        )
