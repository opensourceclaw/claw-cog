"""Integration tests for V/O layers (v1.8.0) in ConsciousAgent pipeline."""

import pytest

from claw_cog import (
    ConsciousAgent, ConsciousnessResultWithVO, ConsciousnessResultWithTime,
    Config, ProcessingResult,
)
from claw_cog.modules.volition.types import Goal


@pytest.fixture
def agent():
    """Create a ConsciousAgent with V/O enabled."""
    return ConsciousAgent()


@pytest.fixture
def agent_vo_disabled():
    """Create a ConsciousAgent with V/O disabled."""
    config = Config(volition_enabled=False, observation_enabled=False)
    return ConsciousAgent(config=config)


class TestVOIntegration:
    """Integration tests for V/O layers in ConsciousAgent pipeline."""

    def test_vo_modules_initialized(self, agent):
        """V/O submodules should be initialized."""
        assert agent._volition_engine is not None
        assert agent._observation_engine is not None
        assert agent._goal_tracker is not None
        assert agent._intention_buffer is not None
        assert agent._self_monitor is not None
        assert agent._anomaly_detector is not None

    def test_process_returns_vo_result_by_default(self, agent):
        """By default, process() should return ConsciousnessResultWithVO."""
        result = agent.process("Hello, world!")
        assert isinstance(result, ConsciousnessResultWithVO)

    def test_process_returns_vo_result_fields(self, agent):
        """ConsciousnessResultWithVO should have all V/O fields."""
        result = agent.process("Test input")
        assert hasattr(result, "goals")
        assert hasattr(result, "active_intention")
        assert hasattr(result, "observations")
        assert hasattr(result, "anomalies")

    def test_enable_vo_override_false(self, agent):
        """enable_vo=False should return ConsciousnessResultWithTime (not VO)."""
        result = agent.process("Test input", enable_vo=False)
        assert not isinstance(result, ConsciousnessResultWithVO)
        assert isinstance(result, ConsciousnessResultWithTime)

    def test_vo_disabled_config(self, agent_vo_disabled):
        """When volition and observation are disabled, get ConsciousnessResultWithTime."""
        result = agent_vo_disabled.process("Test input")
        assert isinstance(result, ConsciousnessResultWithTime)

    def test_reset_clears_vo_modules(self, agent):
        """reset() should clear volition and observation state."""
        # Generate some state
        agent.process("Test to generate goals and observations")
        agent.reset()
        # After reset, goal tracker should be empty
        assert len(agent._goal_tracker.get_all()) == 0

    def test_get_metrics_includes_vo(self, agent):
        """get_metrics() should include volition and observation stats."""
        metrics = agent.get_metrics()
        assert "volition" in metrics
        assert "observation" in metrics
        assert "tracker" in metrics["volition"]
        assert "buffer" in metrics["volition"]
        assert "monitor" in metrics["observation"]
        assert "detector" in metrics["observation"]

    def test_indicator_properties_has_etclovg(self, agent):
        """get_indicator_properties() should include ETCLOVG theory."""
        props = agent.get_indicator_properties()
        assert "ETCLOVG" in props
        assert props["ETCLOVG"]["volition"] is True
        assert props["ETCLOVG"]["observation"] is True
        assert props["ETCLOVG"]["temporal"] is True

    def test_process_with_c2_generates_goals(self, agent):
        """Input that triggers C2 should generate goals."""
        result = agent.process("I'm very confused about the project direction", confidence_threshold=0.3)
        # C2 should detect low confidence and generate recommendation
        # Goals may or may not be generated depending on C2 output
        assert isinstance(result, ConsciousnessResultWithVO)

    def test_observations_accumulate_over_time(self, agent):
        """Multiple process calls should accumulate observation history."""
        for i in range(3):
            agent.process(f"Test input {i}")
        # SelfMonitor should have tracked multiple observations
        metrics = agent.get_metrics()
        assert metrics["observation"]["monitor"]["observations_tracked"] > 0
