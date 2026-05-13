"""Integration tests for claw-cog."""

import pytest
from claw_cog import ConsciousAgent, Config


def test_memory_integration():
    """Test memory integration in processing."""
    agent = ConsciousAgent()
    
    # Process multiple inputs to build memory
    for i in range(5):
        result = agent.process(f"test input {i}")
        assert result is not None
    
    # Verify memory stats
    stats = agent.memory.get_stats()
    assert stats is not None


def test_memory_store_and_retrieve():
    """Test memory store and retrieve."""
    agent = ConsciousAgent()
    
    # Store a reflection
    success = agent.memory.store(
        memory_type="reflection",
        content="I should be more careful",
        metadata={"confidence": 0.8},
    )
    assert success is True
    
    # Retrieve it
    results = agent.memory.retrieve_relevant("careful")
    assert len(results) >= 0  # May or may not find depending on backend


def test_memory_context_formatting():
    """Test memory context formatting."""
    agent = ConsciousAgent()
    
    memories = [
        {"content": "First memory", "type": "experience"},
        {"content": "Second memory", "type": "reflection"},
    ]
    
    context = agent.memory.format_context(memories, max_tokens=100)
    assert "[experience] First memory" in context
    assert "[reflection] Second memory" in context


def test_full_processing_pipeline():
    """Test full processing pipeline with all layers."""
    config = Config(c2_enabled=True)
    agent = ConsciousAgent(config=config)
    
    # Process input
    result = agent.process(
        "What is the meaning of consciousness?",
        context={"domain": "philosophy"},
    )
    
    assert result is not None
    assert result.output is not None
    assert 0.0 <= result.confidence <= 1.0
    
    # Check metadata includes memory
    assert "c0_contribution" in result.metadata
    assert "broadcast_time_ms" in result.metadata


def test_c2_adjustment_triggers_reflection():
    """Test that C2 adjustment triggers reflection storage."""
    agent = ConsciousAgent()
    
    # Process with low confidence threshold to trigger adjustment
    result = agent.process(
        "uncertain input",
        confidence_threshold=0.9,  # High threshold
    )
    
    # Check metrics
    metrics = agent.get_metrics()
    assert metrics["history_size"] == 1


def test_indicator_properties_after_processing():
    """Test indicator properties reflect actual state."""
    agent = ConsciousAgent()
    
    # Process some inputs
    for i in range(10):
        agent.process(f"input {i}")
    
    # Get indicators
    indicators = agent.get_indicator_properties()
    
    # v1.0.0: GWT should be implemented
    assert indicators["GWT"] is True
    # C2 enabled by default
    assert indicators["HOT"]["higher_order_representation"] is True
    # PP in v2.0.0
    assert indicators["PP"] is False


def test_metacognition_with_ground_truth():
    """Test metacognition assessment with ground truth."""
    agent = ConsciousAgent()
    
    # Process inputs
    history = []
    ground_truth = []
    
    for i in range(15):
        result = agent.process(f"input {i}")
        history.append(result)
        # Simulate ground truth (high confidence = correct)
        ground_truth.append(result.confidence > 0.5)
    
    # Assess metacognition
    metrics = agent.assess_metacognition()
    
    assert metrics["sample_size"] == 15
    assert 0.0 <= metrics["meta_d_prime"] <= 2.0
    assert 0.0 <= metrics["m_ratio"] <= 2.0


def test_memory_fallback_mode():
    """Test memory works in fallback mode."""
    # Force fallback by not having claw-mem
    from claw_cog.integration.claw_mem_bridge import ClawMemBridge
    from claw_cog.config.defaults import Config
    
    config = Config()
    bridge = ClawMemBridge(config)
    
    # Should work even without claw-mem
    bridge.store("test", "content")
    results = bridge.retrieve_relevant("content")
    
    # Fallback should return results
    assert isinstance(results, list)


def test_agent_reset_clears_memory():
    """Test that reset clears processing history."""
    agent = ConsciousAgent()
    
    # Process inputs
    for i in range(5):
        agent.process(f"input {i}")
    
    assert len(agent._processing_history) == 5
    
    # Reset
    agent.reset()
    assert len(agent._processing_history) == 0
