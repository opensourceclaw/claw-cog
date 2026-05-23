"""
Tests for claw_cog.execution.handlers (Memory, Learning, External).
"""
import pytest
from claw_cog.execution import Action, ExecutionContext
from claw_cog.execution.handlers import (
    MemoryActionHandler, LearningActionHandler, ExternalActionHandler,
)


@pytest.fixture
def ctx():
    return ExecutionContext()


# ── MemoryActionHandler ────────────────────────────────────────────────────────


class TestMemoryActionHandler:
    def test_can_handle_store(self):
        h = MemoryActionHandler()
        assert h.can_handle(Action(action_type="store_memory"))

    def test_can_handle_retrieve(self):
        h = MemoryActionHandler()
        assert h.can_handle(Action(action_type="retrieve_memory"))

    def test_can_handle_unknown(self):
        h = MemoryActionHandler()
        assert not h.can_handle(Action(action_type="nope"))

    def test_store_and_retrieve(self, ctx):
        h = MemoryActionHandler()
        action = Action(action_type="store_memory", parameters={"key": "k1", "content": "v1"})
        result = h.execute(action, ctx)
        assert result.success
        assert result.output["status"] == "stored"

        # Retrieve
        action2 = Action(action_type="retrieve_memory", parameters={"key": "k1"})
        result2 = h.execute(action2, ctx)
        assert result2.success
        assert result2.output["found"] is True
        assert result2.output["content"] == "v1"

    def test_retrieve_nonexistent(self, ctx):
        h = MemoryActionHandler()
        action = Action(action_type="retrieve_memory", parameters={"key": "nope"})
        result = h.execute(action, ctx)
        assert result.success
        assert result.output["found"] is False

    def test_update(self, ctx):
        h = MemoryActionHandler()
        h.execute(Action(action_type="store_memory", parameters={"key": "k", "content": "old"}), ctx)
        result = h.execute(Action(action_type="update_memory",
                                  parameters={"key": "k", "content": "new"}), ctx)
        assert result.success
        assert result.output["status"] == "updated"

        # Verify
        result2 = h.execute(Action(action_type="retrieve_memory",
                                   parameters={"key": "k"}), ctx)
        assert result2.output["content"] == "new"

    def test_delete(self, ctx):
        h = MemoryActionHandler()
        h.execute(Action(action_type="store_memory", parameters={"key": "k", "content": "v"}), ctx)
        result = h.execute(Action(action_type="delete_memory", parameters={"key": "k"}), ctx)
        assert result.success
        assert result.output["status"] == "deleted"

        result2 = h.execute(Action(action_type="retrieve_memory",
                                   parameters={"key": "k"}), ctx)
        assert not result2.output["found"]

    def test_rollback_store(self, ctx):
        h = MemoryActionHandler()
        action = Action(action_type="store_memory", parameters={"key": "k", "content": "original"})
        result = h.execute(action, ctx)
        assert h.rollback(action, result.output)

    def test_unsupported_action(self, ctx):
        h = MemoryActionHandler()
        action = Action(action_type="bogus_memory")
        result = h.execute(action, ctx)
        assert not result.success


# ── LearningActionHandler ──────────────────────────────────────────────────────


class TestLearningActionHandler:
    def test_can_handle_feedback(self):
        h = LearningActionHandler()
        assert h.can_handle(Action(action_type="feedback"))

    def test_can_handle_update_policy(self):
        h = LearningActionHandler()
        assert h.can_handle(Action(action_type="update_policy"))

    def test_can_handle_unknown(self):
        h = LearningActionHandler()
        assert not h.can_handle(Action(action_type="nope"))

    def test_process_feedback(self, ctx):
        h = LearningActionHandler()
        action = Action(action_type="feedback", parameters={
            "policy_key": "review", "signal": "positive", "confidence": 0.8,
        })
        result = h.execute(action, ctx)
        assert result.success
        assert result.output["status"] == "feedback_recorded"

    def test_get_feedback(self, ctx):
        h = LearningActionHandler()
        h.execute(Action(action_type="feedback", parameters={"policy_key": "p1"}), ctx)
        h.execute(Action(action_type="feedback", parameters={"policy_key": "p1"}), ctx)
        assert len(h.get_feedback("p1")) == 2

    def test_update_policy(self, ctx):
        h = LearningActionHandler()
        action = Action(action_type="update_policy", parameters={
            "policy_key": "review", "policy": {"threshold": 0.9},
        })
        result = h.execute(action, ctx)
        assert result.success
        assert result.output["status"] == "policy_updated"

    def test_get_policy(self, ctx):
        h = LearningActionHandler()
        action = Action(action_type="update_policy", parameters={
            "policy_key": "test", "policy": {"x": 1},
        })
        h.execute(action, ctx)
        policy = h.get_policy("test")
        assert policy["policy"] == {"x": 1}

    def test_rollback_feedback(self, ctx):
        h = LearningActionHandler()
        action = Action(action_type="feedback", parameters={"policy_key": "p1"})
        result = h.execute(action, ctx)
        assert h.rollback(action, result.output)


# ── ExternalActionHandler ──────────────────────────────────────────────────────


class TestExternalActionHandler:
    def test_can_handle_api_call(self):
        h = ExternalActionHandler()
        assert h.can_handle(Action(action_type="api_call"))

    def test_can_handle_notification(self):
        h = ExternalActionHandler()
        assert h.can_handle(Action(action_type="notification"))

    def test_can_handle_unknown(self):
        h = ExternalActionHandler()
        assert not h.can_handle(Action(action_type="nope"))

    def test_api_call_safe_url(self, ctx):
        h = ExternalActionHandler()
        action = Action(action_type="api_call", parameters={
            "url": "https://api.example.com/data", "method": "POST",
        })
        result = h.execute(action, ctx)
        assert result.success
        assert result.output["status"] == "accepted"

    def test_api_call_blocked_localhost(self, ctx):
        h = ExternalActionHandler()
        action = Action(action_type="api_call", parameters={
            "url": "http://localhost:8080/admin",
        })
        result = h.execute(action, ctx)
        assert not result.success
        assert "Blocked" in result.error

    def test_api_call_blocked_file_scheme(self, ctx):
        h = ExternalActionHandler()
        action = Action(action_type="api_call", parameters={
            "url": "file:///etc/passwd",
        })
        result = h.execute(action, ctx)
        assert not result.success

    def test_notification(self, ctx):
        h = ExternalActionHandler()
        action = Action(action_type="notification", parameters={
            "message": "Task completed", "channel": "email",
        })
        result = h.execute(action, ctx)
        assert result.success
        assert result.output["channel"] == "email"

    def test_rollback(self, ctx):
        h = ExternalActionHandler()
        action = Action(action_type="notification", parameters={
            "message": "test",
        })
        h.execute(action, ctx)
        assert h.rollback(action, {})

    def test_call_log(self, ctx):
        h = ExternalActionHandler()
        h.execute(Action(action_type="notification"), ctx)
        h.execute(Action(action_type="subscription"), ctx)  # unknown type, should fail
        assert len(h.get_call_log()) >= 1
