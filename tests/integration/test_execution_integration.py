"""
Integration tests for claw-cog Execution Layer with ConsciousAgent.
"""
import pytest
from claw_cog import ConsciousAgent
from claw_cog.execution import Action, ActionExecutor, ExecutionContext, ActionResult
from claw_cog.execution.handlers import (
    MemoryActionHandler, LearningActionHandler, ExternalActionHandler,
)


class TestExecutionIntegration:
    """Test execution layer integration with ConsciousAgent."""

    def test_agent_has_executor_field(self):
        agent = ConsciousAgent()
        assert agent.executor is None

    def test_enable_execution_defaults(self):
        agent = ConsciousAgent()
        executor = agent.enable_execution()
        assert executor is not None
        assert agent.executor is executor
        assert len(executor.list_handlers()) >= 2

    def test_enable_execution_with_custom_handlers(self):
        agent = ConsciousAgent()
        handlers = [MemoryActionHandler(), ExternalActionHandler()]
        executor = agent.enable_execution(handlers=handlers)
        assert len(executor.list_handlers()) >= 2

    def test_process_and_execute_basic(self):
        agent = ConsciousAgent()
        agent.enable_execution()
        result = agent.process_and_execute("Hello, world!")
        assert result is not None

    def test_extract_actions_from_vo_result(self):
        agent = ConsciousAgent()
        # Process input that triggers VO processing
        result = agent.process("Deploy the application to production",
                                confidence_threshold=0.5)
        actions = agent._extract_actions(result)
        assert isinstance(actions, list)

    def test_execution_context_chain(self):
        """Test full execution pipeline with context."""
        executor = ActionExecutor()
        executor.register_handler("memory", MemoryActionHandler())
        executor.register_handler("learning_handler", LearningActionHandler())

        ctx = ExecutionContext()
        action = Action(action_type="memory", description="Integration test action")
        result = executor.execute(action, context=ctx)

        assert result.success
        assert ctx.get_trace()
        assert ctx.get_action(action.action_id) is not None

    def test_rollback_manager_integration(self):
        """Test rollback manager within executor context."""
        executor = ActionExecutor()
        executor.register_handler("memory", MemoryActionHandler())

        action = Action(action_type="memory", parameters={
            "key": "important", "content": "critical data",
        })
        result = executor.execute(action)
        assert result.success

        assert executor.rollback(action)

    def test_multi_handler_batch(self):
        """Test batch execution across multiple handler types."""
        executor = ActionExecutor()
        executor.register_handler("memory_handler", MemoryActionHandler())
        executor.register_handler("learning_handler", LearningActionHandler())
        executor.register_handler("external_handler", ExternalActionHandler())

        actions = [
            Action(action_type="store_memory", parameters={"key": "batch1", "content": "v1"}),
            Action(action_type="feedback", parameters={"policy_key": "test"}),
            Action(action_type="notification", parameters={"message": "batch done"}),
        ]
        results = executor.execute_batch(actions)
        assert len(results) == 3
        assert all(r.success for r in results)
