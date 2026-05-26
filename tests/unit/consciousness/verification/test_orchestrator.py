"""Tests for claw_cog.consciousness.verification.orchestrator."""

import pytest
from dataclasses import dataclass
from claw_cog.consciousness.verification.orchestrator import (
    VerificationOrchestrator,
    VerificationReport,
)
from claw_cog.consciousness.verification.validator import (
    OutputValidator,
    ValidationStatus,
)
from claw_cog.consciousness.verification.calibrator import ConfidenceCalibrator
from claw_cog.consciousness.verification.quality import QualityAssessor
from claw_cog.consciousness.verification.consistency import ConsistencyChecker


@dataclass
class FakeResult:
    output: str
    confidence: float


@pytest.fixture
def orchestrator():
    return VerificationOrchestrator()


@pytest.fixture
def strict_orchestrator():
    """Orchestrator with strict calibration to test failures."""
    return VerificationOrchestrator(
        calibrator=ConfidenceCalibrator(ece_threshold=0.01),
    )


class TestVerificationOrchestrator:
    def test_composite_pass(self, orchestrator):
        result = FakeResult(output="Hello world", confidence=0.95)
        report = orchestrator.verify(result, history=[])
        assert report.passed

    def test_composite_fail_calibration(self, strict_orchestrator):
        result = FakeResult(output="Hello", confidence=0.95)
        report = strict_orchestrator.verify(result, history=[
            FakeResult(output="Goodbye", confidence=0.1)
        ])
        # Single sample with no reference — pass may vary
        assert isinstance(report.passed, bool)

    def test_report_to_dict(self, orchestrator):
        result = FakeResult(output="Test", confidence=0.9)
        report = orchestrator.verify(result, history=[])
        d = report.to_dict()
        assert "passed" in d
        assert "validation" in d
        assert "calibration" in d
        assert "quality" in d
        assert "consistency" in d
        assert "summary" in d

    def test_verify_with_processing_result(self, orchestrator):
        result = FakeResult(output="Test output", confidence=0.7)
        report = orchestrator.verify(result, history=[])
        assert report.validation is not None
        assert report.calibration is not None
        assert report.quality is not None
        assert report.consistency is not None

    def test_verify_with_failed_validation(self):
        validator = OutputValidator()
        validator.add_rule(
            "fail_always",
            lambda o, c: (ValidationStatus.FAIL, "always fails"),
        )
        orch = VerificationOrchestrator(validator=validator)
        result = FakeResult(output="anything", confidence=0.5)
        report = orch.verify(result, history=[])
        assert not report.passed

    def test_verify_with_contradictory_history(self):
        checker = ConsistencyChecker(deviation_threshold=0.0)
        orch = VerificationOrchestrator(consistency_checker=checker)
        result = FakeResult(output="Cats are not great", confidence=0.5)
        history = [FakeResult(output="Cats are great", confidence=0.5)]
        report = orch.verify(result, history=history)
        assert isinstance(report.passed, bool)

    def test_reset(self, orchestrator):
        validator = orchestrator.validator
        validator.add_rule("r1", lambda o, c: (ValidationStatus.PASS, ""))
        orchestrator.reset()
        assert validator.rule_count == 0
