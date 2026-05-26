"""Integration tests for verification layer and ConsciousAgent."""

import pytest
from claw_cog import (
    ConsciousAgent,
    VerificationOrchestrator,
    VerificationReport,
)
from claw_cog.config.defaults import Config


@pytest.fixture
def agent():
    return ConsciousAgent()


@pytest.fixture
def agent_with_verification_disabled():
    config = Config(verification_enabled=False)
    return ConsciousAgent(config=config)


class TestVerificationAgentIntegration:
    def test_verifier_property(self, agent):
        verifier = agent.verifier
        assert isinstance(verifier, VerificationOrchestrator)

    def test_verify_method(self, agent):
        result = agent.process("Hello world")
        report = agent.verify(result)
        assert isinstance(report, VerificationReport)

    def test_verify_with_history(self, agent):
        agent.process("First input")
        result = agent.process("Second input")
        report = agent.verify(result)
        assert isinstance(report, VerificationReport)

    def test_process_attaches_verification_metadata(self, agent):
        result = agent.process("Test input with verification")
        assert "verification" in result.metadata
        assert "passed" in result.metadata["verification"]
        assert "summary" in result.metadata["verification"]

    def test_verification_disabled_no_metadata(self, agent_with_verification_disabled):
        result = agent_with_verification_disabled.process("Test input")
        assert "verification" not in result.metadata

    def test_reset_clears_verifier(self, agent):
        agent.verifier.validator.add_rule(
            "test_rule",
            lambda o, c: (__import__("claw_cog.consciousness.verification.validator", fromlist=["ValidationStatus"]).ValidationStatus.PASS, ""),
        )
        agent.reset()
        assert agent.verifier.validator.rule_count == 0

    def test_vo_result_verification(self, agent):
        result = agent.process("Schedule meeting at 3pm", enable_vo=True)
        assert "verification" in result.metadata

    def test_multiple_process_verification(self, agent):
        for i in range(3):
            result = agent.process(f"Input {i}")
            assert "verification" in result.metadata
            assert isinstance(agent.verify(result), VerificationReport)
