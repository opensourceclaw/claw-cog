"""Tests for claw_cog.consciousness.governance.policy."""

import pytest
from claw_cog.consciousness.governance.policy import (
    PolicyEnforcer, PolicyResult, PolicyDecision,
)
from claw_cog.consciousness.governance.permission import Role


class TestPolicyEnforcer:
    @pytest.fixture
    def enforcer(self):
        return PolicyEnforcer()

    def test_evaluate_input_safe(self, enforcer):
        result = enforcer.evaluate_input("Hello world")
        assert result.allowed is True
        assert result.decision == PolicyDecision.ALLOWED

    def test_evaluate_input_sqli_blocked(self, enforcer):
        result = enforcer.evaluate_input("DROP TABLE users")
        assert result.allowed is False
        assert result.decision == PolicyDecision.DENIED

    def test_evaluate_input_delete_restricted(self, enforcer):
        result = enforcer.evaluate_input("delete temporary files")
        assert result.decision in (PolicyDecision.RESTRICTED, PolicyDecision.DENIED)

    def test_evaluate_action_allowed(self, enforcer):
        result = enforcer.evaluate_action("read file", role=Role.ASSISTANT)
        assert result.allowed is True

    def test_evaluate_action_delete_critical(self, enforcer):
        result = enforcer.evaluate_action("delete all records", role=Role.USER)
        assert result.allowed is False

    def test_evaluate_output_safe(self, enforcer):
        result = enforcer.evaluate_output("The result is 42")
        assert result.allowed is True

    def test_evaluate_output_sensitive(self, enforcer):
        result = enforcer.evaluate_output("My password: hunter2")
        assert result.allowed is False

    def test_get_audit_summary(self, enforcer):
        enforcer.evaluate_input("test")
        enforcer.evaluate_output("test")
        summary = enforcer.get_audit_summary()
        assert summary["total"] >= 2

    def test_reset(self, enforcer):
        enforcer.evaluate_input("test")
        enforcer.reset()
        assert enforcer.get_audit_summary()["total"] == 0
