"""Tests for claw_cog.consciousness.governance.guardrails."""

import pytest
from claw_cog.consciousness.governance.guardrails.input_filter import InputFilter
from claw_cog.consciousness.governance.guardrails.output_filter import OutputFilter
from claw_cog.consciousness.governance.guardrails.behavior_constraint import BehaviorConstraint


class TestInputFilter:
    @pytest.fixture
    def f(self):
        return InputFilter()

    def test_safe_input(self, f):
        safe, content, reason = f.filter("Hello world")
        assert safe is True
        assert reason is None

    def test_blocked_drop_table(self, f):
        safe, content, reason = f.filter("DROP TABLE users")
        assert safe is False
        assert reason is not None

    def test_blocked_script(self, f):
        safe, content, reason = f.filter("<script>alert(1)</script>")
        assert safe is False

    def test_sanitize_eval(self, f):
        safe, content, reason = f.filter("Use eval(code) to run")
        assert safe is True
        assert "SANITIZED" in content

    def test_length_limit(self, f):
        long_input = "x" * 20000
        safe, content, reason = f.filter(long_input)
        assert safe is False

    def test_empty_input(self, f):
        safe, content, reason = f.filter("")
        assert safe is True

    def test_none_input(self, f):
        safe, content, reason = f.filter(None)
        assert safe is True


class TestOutputFilter:
    @pytest.fixture
    def f(self):
        return OutputFilter()

    def test_safe_output(self, f):
        safe, content, reason = f.filter("The answer is 42")
        assert safe is True

    def test_sensitive_password(self, f):
        safe, content, reason = f.filter("My password: secret123")
        assert safe is False

    def test_sanitize_email(self, f):
        safe, content, reason = f.filter("Email: user@example.com")
        assert safe is True
        assert "user@example.com" not in content

    def test_sensitive_api_key(self, f):
        safe, content, reason = f.filter("api_key=sk-abc123xyz456")
        assert safe is False

    def test_empty(self, f):
        safe, content, reason = f.filter("")
        assert safe is True


class TestBehaviorConstraint:
    @pytest.fixture
    def bc(self):
        return BehaviorConstraint()

    def test_check_allowed(self, bc):
        allowed, reason = bc.check("read file")
        assert allowed is True

    def test_check_denied_pattern(self, bc):
        allowed, reason = bc.check("run rm -rf /")
        assert allowed is False

    def test_deny_operation(self, bc):
        bc.deny_operation("risky_op")
        allowed, reason = bc.check("any command", operation_type="risky_op")
        assert allowed is False

    def test_allow_operation(self, bc):
        bc.deny_operation("temp_op")
        assert bc.allow_operation("temp_op")
        allowed, _ = bc.check("any", operation_type="temp_op")
        assert allowed is True

    def test_get_denied_operations(self, bc):
        ops = bc.get_denied_operations()
        assert "sudo_command" in ops
