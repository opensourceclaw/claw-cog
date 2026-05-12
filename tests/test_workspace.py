"""Test GlobalWorkspace functionality."""

import pytest
from claw_cog.core.workspace import GlobalWorkspace, C1Result
from claw_cog.config.defaults import Config


def test_workspace_initialization():
    """Test workspace can be initialized."""
    config = Config()
    workspace = GlobalWorkspace(config)
    assert workspace is not None


def test_workspace_subscribe():
    """Test subscribing modules."""
    config = Config()
    workspace = GlobalWorkspace(config)

    def dummy_module(content):
        return {"processed": content}

    workspace.subscribe(dummy_module)
    metrics = workspace.get_metrics()
    assert metrics["subscriber_count"] == 1


def test_workspace_max_subscribers():
    """Test max subscriber limit."""
    config = Config(workspace_max_subscribers=2)
    workspace = GlobalWorkspace(config)

    # Should be able to add 2
    workspace.subscribe(lambda x: x)
    workspace.subscribe(lambda x: x)

    # 3rd should be rejected
    workspace.subscribe(lambda x: x)

    metrics = workspace.get_metrics()
    assert metrics["subscriber_count"] == 2


def test_workspace_process():
    """Test workspace processing."""
    config = Config()
    workspace = GlobalWorkspace(config)

    result = workspace.process(
        input="test",
        c0_output="c0 result",
        context=None,
    )

    assert result is not None
    assert result.output is not None
    assert 0.0 <= result.confidence <= 1.0


def test_workspace_broadcast():
    """Test broadcast mechanism."""
    config = Config()
    workspace = GlobalWorkspace(config)

    received = []

    def capture_module(content):
        received.append(content)
        return {"status": "ok"}

    workspace.subscribe(capture_module)
    workspace.process("test input", None, None)

    assert len(received) == 1


def test_workspace_metrics():
    """Test workspace metrics."""
    config = Config()
    workspace = GlobalWorkspace(config)

    # Process a few times
    for i in range(5):
        workspace.process(f"input {i}", None, None)

    metrics = workspace.get_metrics()
    assert metrics["total_broadcasts"] == 5
    assert metrics["avg_broadcast_time_ms"] >= 0


def test_workspace_indicators():
    """Test indicator methods."""
    config = Config()
    workspace = GlobalWorkspace(config)

    assert workspace.is_implemented() is True
    assert workspace.has_attention_mechanism() is True


def test_workspace_clear_history():
    """Test clearing history."""
    config = Config()
    workspace = GlobalWorkspace(config)

    # Process a few times
    for i in range(3):
        workspace.process(f"input {i}", None, None)

    assert len(workspace._broadcast_history) == 3

    workspace.clear_history()
    assert len(workspace._broadcast_history) == 0


def test_broadcast_subscriber_error():
    """Cover subscriber error handling in _broadcast (lines 190-192)."""
    config = Config()
    workspace = GlobalWorkspace(config)

    def error_module(content):
        raise ValueError("intentional error")

    workspace.subscribe(error_module)
    result = workspace.process("test input", None, None)

    assert result is not None
    assert isinstance(result, C1Result)


def test_ego_output_integration():
    """Cover ego_output integration in _integrate (lines 164-165)."""
    config = Config()
    workspace = GlobalWorkspace(config)
    result = workspace.process(
        input="test",
        c0_output="c0 result",
        context={"ego_output": "ego decision", "ego_confidence": 0.7},
    )
    assert result is not None
    assert isinstance(result, C1Result)


def test_unsubscribe_non_subscriber():
    """Test unsubscribing a module that is not subscribed."""
    config = Config()
    workspace = GlobalWorkspace(config)

    def dummy(content):
        return content

    # Should not raise error
    workspace.unsubscribe(dummy)
    assert len(workspace._subscribers) == 0
    workspace.subscribe(dummy)
    workspace.unsubscribe(dummy)
    assert len(workspace._subscribers) == 0
