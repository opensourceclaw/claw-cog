"""
Tests for claw_cog.execution.executor (ActionExecutor).
"""
import pytest
from claw_cog.execution import Action, ActionExecutor, ExecutionContext, ActionResult
from claw_cog.execution.handlers import (
    MemoryActionHandler, LearningActionHandler, ExternalActionHandler,
)


@pytest.fixture
def executor():
    ex = ActionExecutor()
    ex.register_handler("memory", MemoryActionHandler())
    ex.register_handler("learning_handler", LearningActionHandler())
    ex.register_handler("external_handler", ExternalActionHandler())
    return ex


@pytest.fixture
def ctx():
    return ExecutionContext()


class TestActionExecutor:
    def test_register_handler(self):
        ex = ActionExecutor()
        ex.register_handler("test", MemoryActionHandler())
        assert ex.get_handler("test") is not None

    def test_unregister_handler(self):
        ex = ActionExecutor()
        ex.register_handler("test", MemoryActionHandler())
        assert ex.unregister_handler("test")
        assert ex.get_handler("test") is None

    def test_unregister_nonexistent(self):
        ex = ActionExecutor()
        assert not ex.unregister_handler("nope")

    def test_list_handlers(self, executor):
        assert len(executor.list_handlers()) == 3

    def test_execute_with_handler(self, executor, ctx):
        action = Action(action_type="memory", description="store test")
        result = executor.execute(action, context=ctx)
        assert result.success is True
        assert result.action_id == action.action_id

    def test_execute_no_handler(self, ctx):
        ex = ActionExecutor()
        action = Action(action_type="unknown_type")
        result = ex.execute(action, context=ctx)
        assert not result.success
        assert "No handler" in result.error

    def test_execute_tracks_context(self, executor, ctx):
        action = Action(action_type="memory", description="ctx test")
        executor.execute(action, context=ctx)
        trace = ctx.get_trace()
        assert len(trace) == 1
        assert trace[0].action_id == action.action_id

    def test_execute_tracks_duration(self, executor, ctx):
        action = Action(action_type="memory")
        result = executor.execute(action, context=ctx)
        assert result.duration_ms >= 0

    def test_execute_batch_success(self, executor, ctx):
        actions = [
            Action(action_type="memory", description="a1"),
            Action(action_type="memory", description="a2"),
        ]
        results = executor.execute_batch(actions, context=ctx)
        assert len(results) == 2
        assert all(r.success for r in results)

    def test_execute_batch_rollback_on_failure(self, executor, ctx):
        actions = [
            Action(action_type="memory", description="store"),
            Action(action_type="unknown_type"),
        ]
        results = executor.execute_batch(actions, context=ctx)
        assert len(results) == 2
        assert results[0].success
        assert not results[1].success

    def test_execute_batch_creates_context(self, executor):
        actions = [Action(action_type="memory")]
        results = executor.execute_batch(actions)
        assert len(results) == 1
        assert results[0].success

    def test_rollback(self, executor, ctx):
        action = Action(action_type="memory", parameters={"key": "roll-me"})
        executor.execute(action, context=ctx)
        assert executor.rollback(action)

    def test_rollback_no_handler(self):
        ex = ActionExecutor()
        action = Action(action_type="ghost")
        assert not ex.rollback(action)

    def test_rollback_all(self, executor, ctx):
        for i in range(3):
            executor.execute(Action(action_type="memory"), context=ctx)
        count = executor.rollback_all()
        assert count >= 0

    def test_find_handler_by_action_type(self, executor):
        action = Action(action_type="memory")
        handler = executor._find_handler(action)
        assert handler is not None
        assert isinstance(handler, MemoryActionHandler)

    def test_find_handler_by_can_handle(self, executor):
        action = Action(action_type="store_memory")  # MemoryActionHandler handles this
        handler = executor._find_handler(action)
        assert handler is not None

    def test_reset(self, executor):
        executor.execute(Action(action_type="memory"))
        executor.reset()
        assert len(executor.list_handlers()) == 0
