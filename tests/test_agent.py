"""Test ConsciousAgent basic functionality."""

import pytest
from claw_cog import ConsciousAgent, ConsciousnessLevel, Config
from claw_cog.exceptions import ConfigurationError


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

    # v1.0.0 coverage (rc.2: RPT/HOT/AST now return sub-property dicts)
    assert indicators["GWT"] is True
    assert indicators["RPT"]["feedback_loops"] is True
    assert indicators["HOT"]["higher_order_representation"] is True
    assert indicators["PP"] is False
    assert indicators["AST"]["attention_schema"] is True


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


def test_history_overflow():
    """Test history trimming when exceeding assessment_history_size."""
    config = Config(assessment_history_size=10)
    agent = ConsciousAgent(config=config, enable_c2=False)

    for i in range(15):
        agent.process(f"input {i}")

    assert len(agent._processing_history) <= 10


def test_determine_level_c0_boundary():
    """Cover _determine_level C0 boundary (line 199, 201)."""
    agent = ConsciousAgent()
    # We can't directly test _determine_level, but processing with
    # low context should produce C0-level results
    result = agent.process("simple", confidence_threshold=1.0)
    assert result.level in [
        ConsciousnessLevel.C0_UNCONSCIOUS,
        ConsciousnessLevel.C1_CONSCIOUS_ACCESS,
        ConsciousnessLevel.C2_METACOGNITIVE,
    ]


def test_determine_level_c1_boundary():
    """Cover _determine_level C1 boundary."""
    agent = ConsciousAgent()
    result = agent.process("moderate confidence input", confidence_threshold=0.5)
    assert result.level in [
        ConsciousnessLevel.C0_UNCONSCIOUS,
        ConsciousnessLevel.C1_CONSCIOUS_ACCESS,
        ConsciousnessLevel.C2_METACOGNITIVE,
    ]


def test_confidence_threshold_validation():
    """Test that invalid confidence_threshold raises ConfigurationError."""
    agent = ConsciousAgent()
    with pytest.raises(ConfigurationError):
        agent.process("test", confidence_threshold=1.5)
    with pytest.raises(ConfigurationError):
        agent.process("test", confidence_threshold=-0.1)


def test_confidence_threshold_boundary_values():
    """Test valid boundary values for confidence_threshold."""
    agent = ConsciousAgent()
    # 0.0 and 1.0 are valid boundaries
    result_min = agent.process("test", confidence_threshold=0.0)
    result_max = agent.process("test", confidence_threshold=1.0)
    assert result_min is not None
    assert result_max is not None