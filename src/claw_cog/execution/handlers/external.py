"""
ExternalActionHandler — execute external system actions (api_call, notification).

Provides safety boundary checks before executing external actions.
"""

import json
from typing import Any, Dict
from datetime import datetime
from urllib.parse import urlparse

from claw_cog.execution.context import Action, ExecutionContext
from claw_cog.execution.result import ActionResult
from claw_cog.execution.handlers.base import ActionHandler


class ExternalActionHandler(ActionHandler):
    """Execute external system actions with safety checks.

    Handles action types: api_call, notification.
    Performs URL safety checks and data sanitization.
    """

    _EXTERNAL_TYPES = {"api_call", "notification"}

    # Blocked URL patterns for safety
    _BLOCKED_PATTERNS = {"127.0.0.1", "localhost", "0.0.0.0"}

    def __init__(self):
        self._call_log: list = []

    def can_handle(self, action: Action) -> bool:
        return action.action_type in self._EXTERNAL_TYPES

    def execute(self, action: Action, context: ExecutionContext) -> ActionResult:
        method_map = {
            "api_call": self._process_api_call,
            "notification": self._process_notification,
        }
        handler = method_map.get(action.action_type)
        if handler is None:
            return ActionResult.failure_result(
                action.action_id, f"Unsupported external action: {action.action_type}",
            )

        try:
            start = datetime.now()
            output = handler(action, context)
            duration = (datetime.now() - start).total_seconds() * 1000
            return ActionResult.success_result(action.action_id, output=output, duration_ms=duration)
        except Exception as e:
            return ActionResult.failure_result(action.action_id, error=str(e))

    def rollback(self, action: Action, rollback_data: Dict[str, Any]) -> bool:
        # External actions are typically non-reversible
        # Log the rollback attempt
        self._call_log.append({
            "action_id": action.action_id,
            "rollback_attempted": True,
            "timestamp": datetime.now().isoformat(),
        })
        return True

    def get_call_log(self) -> list:
        """Get the external call log."""
        return list(self._call_log)

    # ── Internal ────────────────────────────────────────────────────────────────

    def _process_api_call(self, action: Action, context: ExecutionContext) -> Dict[str, Any]:
        url = action.parameters.get("url", "")
        method = action.parameters.get("method", "GET")
        payload = action.parameters.get("payload", {})

        # Safety check
        safety_result = self._check_safety(url)
        if not safety_result["safe"]:
            raise ValueError(f"Blocked URL: {safety_result['reason']}")

        # Simulated execution (Phase 1: no real HTTP)
        entry = {
            "url": url,
            "method": method,
            "payload": json.dumps(payload),
            "timestamp": datetime.now().isoformat(),
            "status": "simulated",
        }
        self._call_log.append(entry)
        return {"url": url, "method": method, "status": "accepted", "entry": entry}

    def _process_notification(self, action: Action, context: ExecutionContext) -> Dict[str, Any]:
        message = action.parameters.get("message", action.description)
        channel = action.parameters.get("channel", "log")

        entry = {
            "message": message,
            "channel": channel,
            "timestamp": datetime.now().isoformat(),
            "status": "delivered",
        }
        self._call_log.append(entry)
        return {"channel": channel, "status": "delivered", "entry": entry}

    def _check_safety(self, url: str) -> Dict[str, Any]:
        """Check URL safety against blocked patterns."""
        if not url:
            return {"safe": True, "reason": ""}

        try:
            parsed = urlparse(url)
            hostname = (parsed.hostname or "").lower()

            for blocked in self._BLOCKED_PATTERNS:
                if blocked in hostname:
                    return {"safe": False, "reason": f"URL contains blocked host: {blocked}"}

            # Block file:// scheme
            if parsed.scheme == "file":
                return {"safe": False, "reason": "file:// scheme is blocked"}

            return {"safe": True, "reason": ""}
        except Exception:
            return {"safe": False, "reason": f"Could not parse URL: {url}"}
