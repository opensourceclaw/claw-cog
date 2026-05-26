"""Full ETCLOVG pipeline integration test for claw-cog v4.0.0.

Tests the complete pipeline: E (Execution) → T (Time) → C (Conscious) →
L (Learning) → O (Observation) → V (Verification) → G (Governance).
"""

import pytest
from claw_cog import ConsciousAgent, Config


class TestETCLOVGFullPipeline:
    @pytest.fixture
    def agent(self):
        return ConsciousAgent()

    def test_full_pipeline_process(self, agent):
        """Test that process() activates all ETCLOVG layers."""
        result = agent.process("Hello world, schedule meeting at 3pm tomorrow")

        # C: Conscious processing
        assert result.output is not None
        assert 0.0 <= result.confidence <= 1.0

        # V: Verification metadata
        assert "verification" in result.metadata
        assert "passed" in result.metadata["verification"]

        # G: Governance metadata
        assert "governance" in result.metadata
        assert "allowed" in result.metadata["governance"]

    def test_full_pipeline_with_vo(self, agent):
        """Test vo-enabled pipeline produces VO layer outputs."""
        result = agent.process(
            "Schedule daily standup for 2pm, important deadline next Friday",
            enable_vo=True,
        )
        assert hasattr(result, "goals")
        assert hasattr(result, "observations")
        assert hasattr(result, "anomalies")

    def test_verify_after_process(self, agent):
        """Test that verify() works on a processing result."""
        result = agent.process("Test verification step")
        report = agent.verify(result)
        assert hasattr(report, "passed")

    def test_governance_after_process(self, agent):
        """Test that governance layer is active."""
        agent.process("Safe test input")
        summary = agent.governance.get_audit_summary()
        assert summary["total"] >= 1

    def test_verifier_property(self, agent):
        """V: Verification orchestrator available."""
        verifier = agent.verifier
        assert verifier is not None

    def test_governance_property(self, agent):
        """G: Governance enforcer available."""
        assert agent.governance is not None

    def test_execution_layer_available(self, agent):
        """E: Execution layer can be enabled."""
        agent.enable_execution()
        assert agent.executor is not None

    def test_reset_clears_all_layers(self, agent):
        """Reset clears V and G state."""
        agent.process("test")
        agent.reset()
        assert agent.governance.get_audit_summary()["total"] == 0


class TestETCLOVGEdgeCases:
    @pytest.fixture
    def agent(self):
        return ConsciousAgent()

    def test_empty_input(self, agent):
        result = agent.process("")
        assert result.output is not None
        assert "verification" in result.metadata

    def test_very_long_input(self, agent):
        long_input = "x" * 50000
        result = agent.process(long_input)
        assert result.output is not None

    def test_unicode_input(self, agent):
        result = agent.process("你好世界 🎉 こんにちは")
        assert result.output is not None

    def test_numeric_input(self, agent):
        result = agent.process("42")
        assert result.output is not None

    def test_list_input(self, agent):
        result = agent.process(["item1", "item2", "item3"])
        assert result.output is not None

    def test_degraded_governance_disabled(self):
        config = Config(governance_enabled=False, verification_enabled=False)
        agent = ConsciousAgent(config=config)
        result = agent.process("test")
        assert result.output is not None
        assert "governance" not in result.metadata
        assert "verification" not in result.metadata
