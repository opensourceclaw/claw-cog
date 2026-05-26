"""Tests for claw_cog.consciousness.governance.permission."""

import pytest
from claw_cog.consciousness.governance.permission import (
    PermissionController, PermissionDecision, RiskLevel, Role, PermissionResult,
)


class TestPermissionController:
    @pytest.fixture
    def pc(self):
        return PermissionController()

    def test_classify_risk_critical(self, pc):
        assert pc.classify_risk("delete all data") == RiskLevel.CRITICAL

    def test_classify_risk_high(self, pc):
        assert pc.classify_risk("write config file") == RiskLevel.HIGH

    def test_classify_risk_medium(self, pc):
        assert pc.classify_risk("query database") == RiskLevel.MEDIUM

    def test_classify_risk_low(self, pc):
        assert pc.classify_risk("hello world") == RiskLevel.LOW

    def test_assistant_critical_denied(self, pc):
        result = pc.check("delete data", Role.ASSISTANT)
        assert result.decision == PermissionDecision.DENY

    def test_assistant_low_allowed(self, pc):
        result = pc.check("say hello", Role.ASSISTANT)
        assert result.decision == PermissionDecision.ALLOW

    def test_system_critical_warn(self, pc):
        result = pc.check("delete data", Role.SYSTEM)
        assert result.decision == PermissionDecision.WARN

    def test_user_medium_warn(self, pc):
        result = pc.check("read file", Role.USER)
        assert result.decision == PermissionDecision.WARN

    def test_set_role_permission(self, pc):
        pc.set_role_permission(Role.ASSISTANT, RiskLevel.HIGH, PermissionDecision.ALLOW)
        result = pc.check("modify config", Role.ASSISTANT)
        assert result.decision == PermissionDecision.ALLOW

    def test_get_role_permission(self, pc):
        d = pc.get_role_permission(Role.ASSISTANT, RiskLevel.CRITICAL)
        assert d == PermissionDecision.DENY

    def test_result_attributes(self, pc):
        result = pc.check("delete file", Role.USER)
        assert result.role == Role.USER
        assert result.risk_level == RiskLevel.CRITICAL
        assert len(result.reason) > 0
