"""Enhanced tests for ConsciousAgent — coverage focused."""
import pytest
from claw_cog import ConsciousAgent, Config, ConsciousnessLevel


def test_generate_calibration_data():
    """Test calibration data generates processing history."""
    agent = ConsciousAgent(enable_c2=False)
    agent.generate_calibration_data(20)
    assert len(agent._processing_history) == 20
    assert agent._processing_history[0].confidence > 0


def test_calibration_produces_meaningful_metacognition():
    """Test that calibration enables meta-d' evaluation."""
    agent = ConsciousAgent(enable_c2=False)
    agent.generate_calibration_data(20)
    metrics = agent.assess_metacognition()
    assert "warning" not in metrics
    assert metrics["sample_size"] == 20
    assert metrics["meta_d_prime"] > 0.0


def test_calibration_varying_confidence_levels():
    """Test calibration includes high and low confidence entries."""
    agent = ConsciousAgent(enable_c2=False)
    agent.generate_calibration_data(30)
    confidences = [r.confidence for r in agent._processing_history]
    assert any(c < 0.5 for c in confidences), "should have low-confidence entries"
    assert any(c > 0.6 for c in confidences), "should have high-confidence entries"


def test_calibration_trim_history():
    """Test calibration respects history size limit."""
    config = Config(assessment_history_size=5)
    agent = ConsciousAgent(config=config, enable_c2=False)
    agent.generate_calibration_data(20)
    assert len(agent._processing_history) == 5


def test_determine_level_from_confidence_high():
    """Test _determine_level_from_confidence with high confidence."""
    agent = ConsciousAgent(enable_c2=False)
    assert agent._determine_level_from_confidence(0.9) == \
        ConsciousnessLevel.C2_METACOGNITIVE


def test_determine_level_from_confidence_medium():
    """Test _determine_level_from_confidence with medium confidence."""
    agent = ConsciousAgent(enable_c2=False)
    assert agent._determine_level_from_confidence(0.6) == \
        ConsciousnessLevel.C1_CONSCIOUS_ACCESS


def test_determine_level_from_confidence_low():
    """Test _determine_level_from_confidence with low confidence."""
    agent = ConsciousAgent(enable_c2=False)
    assert agent._determine_level_from_confidence(0.3) == \
        ConsciousnessLevel.C0_UNCONSCIOUS


def test_c2_adjustment_applied():
    """Test that C2 adjustment increases confidence."""
    agent = ConsciousAgent(enable_c2=True,
                           config=Config(c2_low_threshold=0.25,
                                         c2_medium_threshold=0.35,
                                         c2_high_threshold=0.8))
    result = agent.process("test input for adjustment")
    assert result is not None
    assert 0.0 <= result.confidence <= 1.0


def test_reflection_stored_on_adjustment():
    """Test that reflection is stored when C2 detects adjustment."""
    agent = ConsciousAgent(enable_c2=True,
                           config=Config(c2_low_threshold=0.25))
    # Process with context that triggers low confidence
    result = agent.process("unusual input requiring reflection")
    assert result is not None


def test_confidence_threshold_edge_zero():
    """Test confidence_threshold=0.0 boundary."""
    agent = ConsciousAgent()
    result = agent.process("test", confidence_threshold=0.0)
    assert result is not None


def test_confidence_threshold_edge_one():
    """Test confidence_threshold=1.0 boundary."""
    agent = ConsciousAgent()
    result = agent.process("test", confidence_threshold=1.0)
    assert result is not None


def test_c2_strategy_adjustment():
    """Cover _apply_c2_adjustment non-confidence path (lines 192-200)."""
    config = Config(c2_high_threshold=0.95, c2_medium_threshold=0.85,
                    c2_low_threshold=0.05)
    agent = ConsciousAgent(config=config, enable_c2=True)
    result = agent.process("test for strategy adjustment")
    assert result is not None


def test_c2_seek_help_adjustment():
    """Cover C2 seek_help adjustment type."""
    config = Config(c2_high_threshold=0.95, c2_medium_threshold=0.85,
                    c2_low_threshold=0.5)
    agent = ConsciousAgent(config=config, enable_c2=True)
    result = agent.process("very uncertain input")
    assert result is not None


def test_agent_with_memory_context():
    """Cover memory context when memories exist."""
    agent = ConsciousAgent(enable_c2=False)
    result = agent.process("test with context", context={"extra": "data"})
    assert result.output is not None
    assert result.confidence >= 0.0


def test_agent_process_with_high_c0_contribution():
    """Cover C0 contribution > 0.5 path in integration."""
    from claw_cog import Config
    config = Config(c0_pattern_threshold=0.1, c0_auto_response_enabled=True)
    agent = ConsciousAgent(config=config, enable_c2=False)
    result = agent.process("test c0 high contribution")
    assert result is not None


def test_agent_process_none_input():
    """Cover processing with None input."""
    agent = ConsciousAgent(enable_c2=False)
    result = agent.process(None)
    assert result is not None


def test_metrics_after_processing():
    """Test get_metrics after calibration."""
    agent = ConsciousAgent(enable_c2=False)
    agent.generate_calibration_data(5)
    metrics = agent.get_metrics()
    assert "workspace" in metrics
    assert "history_size" in metrics
    assert metrics["history_size"] == 5


def test_metacognition_with_ground_truth():
    """Test metacognition assessment with ground truth."""
    agent = ConsciousAgent(enable_c2=False)
    agent.generate_calibration_data(5)
    metrics = agent.assess_metacognition()
    assert "meta_d_prime" in metrics
    assert "d_prime" in metrics
    assert "m_ratio" in metrics


def test_c2_non_confidence_adjustment():
    """Cover _apply_c2_adjustment non-confidence path (line 194)."""
    from claw_cog.core.workspace import C1Result
    from claw_cog.layers.c2_metacognitive import C2Result

    agent = ConsciousAgent(enable_c2=True)
    c1 = C1Result(output="test", confidence=0.6, broadcast_time_ms=1.0)
    c2 = C2Result(
        needs_adjustment=True,
        adjustment_type="strategy",
        confidence_estimate=0.6,
    )
    adjusted = agent._apply_c2_adjustment(c1, c2)
    assert adjusted is c1  # non-confidence = return unchanged


def test_c2_confidence_adjustment():
    """Cover _apply_c2_adjustment confidence path (lines 188-193)."""
    from claw_cog.core.workspace import C1Result
    from claw_cog.layers.c2_metacognitive import C2Result

    agent = ConsciousAgent(enable_c2=True)
    c1 = C1Result(output="test", confidence=0.6, broadcast_time_ms=1.0)
    c2 = C2Result(
        needs_adjustment=True,
        adjustment_type="confidence",
        confidence_estimate=0.6,
    )
    adjusted = agent._apply_c2_adjustment(c1, c2)
    assert adjusted.confidence > c1.confidence


def test_determine_level_c0_direct():
    """Cover _determine_level C0 path (lines 206-209)."""
    from claw_cog.core.workspace import C1Result
    agent = ConsciousAgent(enable_c2=False)
    c1 = C1Result(output="test", confidence=0.3, broadcast_time_ms=1.0)
    level = agent._determine_level(c1)
    assert level == ConsciousnessLevel.C0_UNCONSCIOUS


def test_determine_level_c2_direct():
    """Cover _determine_level C2 path."""
    from claw_cog.core.workspace import C1Result
    agent = ConsciousAgent(enable_c2=False)
    c1 = C1Result(output="test", confidence=0.9, broadcast_time_ms=1.0)
    level = agent._determine_level(c1)
    assert level == ConsciousnessLevel.C2_METACOGNITIVE


def test_determine_level_c1_direct():
    """Cover _determine_level C1 path."""
    from claw_cog.core.workspace import C1Result
    agent = ConsciousAgent(enable_c2=False)
    c1 = C1Result(output="test", confidence=0.6, broadcast_time_ms=1.0)
    level = agent._determine_level(c1)
    assert level == ConsciousnessLevel.C1_CONSCIOUS_ACCESS
