"""Tests for claw_cog.consciousness.governance.boundary."""

import pytest
from claw_cog.consciousness.governance.boundary import (
    SafetyBoundary, BoundaryRule, BoundaryDecision,
)


class TestSafetyBoundary:
    @pytest.fixture
    def boundary(self):
        return SafetyBoundary()

    def test_check_allowed(self, boundary):
        decision, reason = boundary.check("read file", domain="file_system")
        assert decision == BoundaryDecision.ALLOWED

    def test_check_denied_delete(self, boundary):
        decision, reason = boundary.check("rm -rf /tmp", domain="file_system")
        assert decision == BoundaryDecision.DENIED

    def test_check_denied_system(self, boundary):
        decision, reason = boundary.check("shutdown now", domain="system")
        assert decision == BoundaryDecision.DENIED

    def test_check_restricted(self, boundary):
        decision, reason = boundary.check("bind port 80", domain="network")
        assert decision == BoundaryDecision.RESTRICTED

    def test_add_rule(self, boundary):
        boundary.add_rule(BoundaryRule(
            name="test_rule", domain="test",
            denied_operations={"dangerous"},
        ))
        decision, _ = boundary.check("do dangerous things", domain="test")
        assert decision == BoundaryDecision.DENIED

    def test_add_duplicate_rule_raises(self, boundary):
        boundary.add_rule(BoundaryRule(name="unique"))
        with pytest.raises(ValueError):
            boundary.add_rule(BoundaryRule(name="unique"))

    def test_remove_rule(self, boundary):
        boundary.add_rule(BoundaryRule(name="tmp"))
        assert boundary.remove_rule("tmp")
        assert not boundary.remove_rule("nonexistent")

    def test_get_rules(self, boundary):
        rules = boundary.get_rules()
        assert len(rules) > 0
        assert any(r.name == "no_file_system_delete" for r in rules)

    def test_allowed_list_denies_unknown(self, boundary):
        boundary.add_rule(BoundaryRule(
            name="strict_network", domain="network_strict",
            allowed_operations={"ping", "nslookup"},
        ))
        decision, _ = boundary.check("curl google.com", domain="network_strict")
        assert decision == BoundaryDecision.DENIED

    def test_allowed_list_allows_known(self, boundary):
        boundary.add_rule(BoundaryRule(
            name="strict_network2", domain="network_strict2",
            allowed_operations={"ping"},
        ))
        decision, _ = boundary.check("ping google.com", domain="network_strict2")
        assert decision == BoundaryDecision.ALLOWED
