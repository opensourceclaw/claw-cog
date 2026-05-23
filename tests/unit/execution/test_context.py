"""
Tests for claw_cog.execution.context (Action, ExecutionContext).
"""
import pytest
from claw_cog.execution import Action, ExecutionContext


class TestAction:
    def test_default_creation(self):
        a = Action()
        assert len(a.action_id) > 0
        assert a.action_type == ""
        assert a.priority == 5
        assert a.source == "volition"

    def test_custom_creation(self):
        a = Action(
            action_type="memory",
            description="store important data",
            parameters={"key": "val"},
            source="cognition",
            priority=8,
        )
        assert a.action_type == "memory"
        assert a.priority == 8
        assert a.parameters["key"] == "val"

    def test_to_dict(self):
        a = Action(action_type="test", description="test action")
        d = a.to_dict()
        assert d["action_type"] == "test"
        assert d["description"] == "test action"

    def test_from_dict(self):
        d = {"action_type": "recon", "description": "recon action", "priority": 3}
        a = Action.from_dict(d)
        assert a.action_type == "recon"
        assert a.priority == 3

    def test_from_dict_defaults(self):
        a = Action.from_dict({})
        assert a.action_type == ""


class TestExecutionContext:
    def test_default_creation(self):
        ctx = ExecutionContext()
        assert len(ctx.session_id) > 0

    def test_custom_session_id(self):
        ctx = ExecutionContext(session_id="my-session")
        assert ctx.session_id == "my-session"

    def test_start_and_complete_action(self):
        ctx = ExecutionContext()
        action = Action(action_type="test")
        ctx.start_action(action)
        ctx.complete_action(action.action_id, success=True)
        trace = ctx.get_trace()
        assert len(trace) == 1

    def test_complete_with_error(self):
        ctx = ExecutionContext()
        action = Action(action_type="test")
        ctx.start_action(action)
        ctx.complete_action(action.action_id, success=False, error="something broke")
        errors = ctx.get_errors()
        assert action.action_id in errors

    def test_get_action(self):
        ctx = ExecutionContext()
        action = Action(action_type="test")
        ctx.start_action(action)
        found = ctx.get_action(action.action_id)
        assert found is not None
        assert found.action_id == action.action_id

    def test_get_action_nonexistent(self):
        ctx = ExecutionContext()
        assert ctx.get_action("no-such") is None

    def test_get_duration(self):
        ctx = ExecutionContext()
        action = Action(action_type="test")
        ctx.start_action(action)
        duration = ctx.get_duration(action.action_id)
        assert duration is not None
        assert duration >= 0

    def test_get_duration_nonexistent(self):
        ctx = ExecutionContext()
        assert ctx.get_duration("no-such") is None

    def test_create_child(self):
        ctx = ExecutionContext(session_id="parent")
        child = ctx.create_child()
        assert child.parent_context is ctx
        assert child.metadata["parent_session"] == "parent"

    def test_get_all_actions_includes_children(self):
        ctx = ExecutionContext()
        child = ctx.create_child()
        a1 = Action(action_type="parent")
        a2 = Action(action_type="child")
        ctx.start_action(a1)
        child.start_action(a2)
        all_actions = ctx.get_all_actions()
        assert len(all_actions) == 2

    def test_reset(self):
        ctx = ExecutionContext()
        action = Action(action_type="test")
        ctx.start_action(action)
        ctx.reset()
        assert len(ctx.get_trace()) == 0

    def test_to_dict(self):
        ctx = ExecutionContext(session_id="dict-test")
        action = Action(action_type="test")
        ctx.start_action(action)
        d = ctx.to_dict()
        assert d["session_id"] == "dict-test"
        assert len(d["actions"]) == 1
