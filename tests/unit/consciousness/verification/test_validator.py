"""Tests for claw_cog.consciousness.verification.validator."""

import pytest
from claw_cog.consciousness.verification.validator import (
    OutputValidator,
    ValidationResult,
    ValidationStatus,
)


@pytest.fixture
def validator():
    return OutputValidator()


class TestOutputValidator:
    def test_empty_rules_validates_clean(self, validator):
        result = validator.validate("anything")
        assert result.status == ValidationStatus.PASS
        assert result.passed == 0
        assert result.failed == 0

    def test_add_rule(self, validator):
        validator.add_rule(
            "non_empty",
            lambda o, c: (ValidationStatus.PASS if o else ValidationStatus.FAIL, "msg"),
        )
        assert validator.rule_count == 1

    def test_add_duplicate_rule_raises(self, validator):
        validator.add_rule("r1", lambda o, c: (ValidationStatus.PASS, ""))
        with pytest.raises(ValueError):
            validator.add_rule("r1", lambda o, c: (ValidationStatus.PASS, ""))

    def test_remove_rule(self, validator):
        validator.add_rule("r1", lambda o, c: (ValidationStatus.PASS, ""))
        assert validator.remove_rule("r1")
        assert validator.rule_count == 0

    def test_remove_nonexistent_rule(self, validator):
        assert not validator.remove_rule("nonexistent")

    def test_pass_rule(self, validator):
        validator.add_rule(
            "non_empty",
            lambda o, c: (ValidationStatus.PASS if o else ValidationStatus.FAIL, "check"),
        )
        result = validator.validate("hello")
        assert result.status == ValidationStatus.PASS
        assert result.passed == 1
        assert result.failed == 0

    def test_fail_rule(self, validator):
        validator.add_rule(
            "non_empty",
            lambda o, c: (ValidationStatus.PASS if o else ValidationStatus.FAIL, "empty"),
        )
        result = validator.validate(None)
        assert result.status == ValidationStatus.FAIL
        assert result.failed == 1

    def test_warn_rule(self, validator):
        validator.add_rule(
            "len_check",
            lambda o, c: (ValidationStatus.WARN if o and len(str(o)) < 5 else ValidationStatus.PASS, "short"),
        )
        result = validator.validate("hi")
        assert result.status == ValidationStatus.WARN
        assert result.warned == 1

    def test_multiple_rules(self, validator):
        validator.add_rule("r1", lambda o, c: (ValidationStatus.PASS, "ok"))
        validator.add_rule("r2", lambda o, c: (ValidationStatus.FAIL, "bad"))
        result = validator.validate("test")
        assert result.status == ValidationStatus.FAIL
        assert result.passed == 1
        assert result.failed == 1

    def test_rule_exception_handled(self, validator):
        def bad_rule(o, c):
            raise RuntimeError("boom")
        validator.add_rule("bad", bad_rule)
        result = validator.validate("test")
        assert result.failed == 1

    def test_validate_against_matching(self, validator):
        validator.add_rule("r1", lambda o, c: (ValidationStatus.PASS, ""))
        result = validator.validate_against("hello", "hello")
        assert result.status == ValidationStatus.PASS

    def test_validate_against_mismatch(self, validator):
        validator.add_rule("r1", lambda o, c: (ValidationStatus.PASS, ""))
        result = validator.validate_against("hello", "world")
        assert result.status == ValidationStatus.FAIL

    def test_reset(self, validator):
        validator.add_rule("r1", lambda o, c: (ValidationStatus.PASS, ""))
        validator.reset()
        assert validator.rule_count == 0

    def test_context_passed_to_rule(self, validator):
        captured = {}
        def capturing_rule(o, c):
            captured["context"] = c
            return ValidationStatus.PASS, ""
        validator.add_rule("capture", capturing_rule)
        validator.validate("test", {"key": "value"})
        assert captured["context"] == {"key": "value"}
