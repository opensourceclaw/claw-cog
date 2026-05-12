"""Test ConsciousAgent basic functionality."""

import pytest
from claw_cog import ConsciousAgent, ConsciousnessLevel, Config


def test_agent_initialization():
    """Test agent can be initialized."""
    agent = ConsciousAgent()
    assert agent is not None
    assert agent.workspace is not None
    assert agent.layers is not None


def test_agent_with_config():
    """Test agent with custom config."""
    config = Config(
        c2_enabled=False,
        c1_confidence_threshold=0.8,
    )
    agent = ConsciousAgent(config=config)
    assert agent.config.c2_enabled is False
    assert agent.config.c1_confidence_threshold == 0.8


def test_process_simple_input():
    """Test processing simple input."""
    agent = ConsciousAgent()
    result = agent.process("test input")

    assert result is not None
    assert result.output is not None
    assert 0.0 <= result.confidence <= 1.0
    assert result.level in [
        ConsciousnessLevel.C0_UNCONSCIOUS,
        ConsciousnessLevel.C1_CONSCIOUS_ACCESS,
        ConsciousnessLevel.C2_METACOGNITIVE,
    ]


def test_c2_disabled():
    """Test agent with C2 disabled."""
    agent = ConsciousAgent(enable_c2=False)
    assert agent.layers.c2_enabled is False
    assert agent.layers.c2 is None


def test_get_indicator_properties():
    """Test indicator properties retrieval."""
    agent = ConsciousAgent()
    indicators = agent.get_indicator_properties()

    assert "GWT" in indicators
    assert "RPT" in indicators
    assert "HOT" in indicators
    assert "PP" in indicators
    assert "AST" in indicators

    # v1.0.0 coverage
    assert indicators["GWT"] is True  # GlobalWorkspace implemented
    assert indicators["RPT"] is True  # Feedback loops exist
    assert indicators["HOT"] is True  # C2 enabled by default
    assert indicators["PP"] is False  # Not in v1.0.0
    assert indicators["AST"] is True  # Basic attention


def test_get_metrics():
    """Test metrics retrieval."""
    agent = ConsciousAgent()
    metrics = agent.get_metrics()

    assert "workspace" in metrics
    assert "layers" in metrics
    assert "history_size" in metrics


def test_assess_metacognition_insufficient_data():
    """Test metacognition assessment with insufficient data."""
    agent = ConsciousAgent()

    # No processing history
    metrics = agent.assess_metacognition()
    assert metrics["meta_d_prime"] == 0.0
    assert "warning" in metrics


def test_process_multiple_times():
    """Test processing multiple inputs."""
    agent = ConsciousAgent()

    for i in range(15):
        result = agent.process(f"input {i}")
        assert result is not None

    # Now we have enough history
    metrics = agent.assess_metacognition()
    assert metrics["sample_size"] == 15


def test_reset():
    """Test agent reset."""
    agent = ConsciousAgent()

    # Process some inputs
    for i in range(5):
        agent.process(f"input {i}")

    assert len(agent._processing_history) == 5

    # Reset
    agent.reset()
    assert len(agent._processing_history) == 0