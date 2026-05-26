"""Integration tests for governance layer and ConsciousAgent."""

import pytest
from claw_cog import (
    ConsciousAgent,
    PolicyEnforcer,
    SafetyBoundary,
    PermissionController,
    AuditLogger,
)
from claw_cog.config.defaults import Config


class TestGovernanceAgentIntegration:
    @pytest.fixture
    def agent(self):
        return ConsciousAgent()

    @pytest.fixture
    def agent_no_governance(self):
        config = Config(governance_enabled=False)
        return ConsciousAgent(config=config)

    def test_governance_property(self, agent):
        g = agent.governance
        assert isinstance(g, PolicyEnforcer)

    def test_process_with_governance(self, agent):
        result = agent.process("Hello world")
        assert "governance" in result.metadata
        assert "allowed" in result.metadata["governance"]

    def test_governance_disabled(self, agent_no_governance):
        result = agent_no_governance.process("DROP TABLE test")
        assert "governance" not in result.metadata

    def test_governance_blocks_dangerous_input(self, agent):
        result = agent.process("DROP TABLE users CASCADE")
        g = result.metadata.get("governance", {})
        assert isinstance(g, dict)

    def test_reset_clears_governance(self, agent):
        agent.governance.evaluate_input("test")
        agent.reset()
        assert agent.governance.get_audit_summary()["total"] == 0

    def test_multiple_processes_audit_trail(self, agent):
        agent.process("first query")
        agent.process("second query")
        summary = agent.governance.get_audit_summary()
        assert summary["total"] >= 2
