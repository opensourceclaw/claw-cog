"""
Tests for claw_cog.execution.result (ActionResult).
"""
import pytest
from claw_cog.execution.result import ActionResult


class TestActionResult:
    def test_default_creation(self):
        r = ActionResult()
        assert r.action_id == ""
        assert r.success is False
        assert r.duration_ms == 0.0

    def test_success_result_factory(self):
        r = ActionResult.success_result("action-1", output={"data": 42}, duration_ms=150.5)
        assert r.action_id == "action-1"
        assert r.success is True
        assert r.output == {"data": 42}
        assert r.duration_ms == 150.5

    def test_failure_result_factory(self):
        r = ActionResult.failure_result("action-2", error="timeout", duration_ms=3000.0)
        assert r.action_id == "action-2"
        assert r.success is False
        assert r.error == "timeout"
        assert r.duration_ms == 3000.0

    def test_to_dict(self):
        r = ActionResult(
            action_id="a1", success=True, output="done", error=None,
            duration_ms=100.0, rollback_data={"snapshot": "old"},
        )
        d = r.to_dict()
        assert d["action_id"] == "a1"
        assert d["success"] is True
        assert d["output"] == "done"
        assert d["rollback_data"] == {"snapshot": "old"}

    def test_from_dict(self):
        d = {
            "action_id": "recon", "success": True, "output": "ok",
            "error": None, "duration_ms": 50.0, "rollback_data": None,
        }
        r = ActionResult.from_dict(d)
        assert r.action_id == "recon"
        assert r.success is True

    def test_from_dict_defaults(self):
        r = ActionResult.from_dict({})
        assert r.action_id == ""
        assert r.success is False
