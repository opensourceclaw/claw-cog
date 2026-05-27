"""Verification orchestrator — coordinates validation, calibration, quality, and consistency."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import logging

from claw_cog.consciousness.verification.validator import (
    OutputValidator,
    ValidationResult,
    ValidationStatus,
)
from claw_cog.consciousness.verification.calibrator import (
    ConfidenceCalibrator,
    CalibrationResult,
)
from claw_cog.consciousness.verification.quality import (
    QualityAssessor,
    QualityResult,
    QualityScore,
)
from claw_cog.consciousness.verification.consistency import (
    ConsistencyChecker,
    ConsistencyResult,
)

logger = logging.getLogger(__name__)


@dataclass
class VerificationReport:
    """Composite verification report combining all sub-results.

    Attributes:
        passed: Whether overall verification passed.
        validation: Output validation result.
        calibration: Confidence calibration result.
        quality: Quality assessment result.
        consistency: Consistency check result.
        summary: Human-readable summary string.
    """

    passed: bool = True
    validation: Optional[ValidationResult] = None
    calibration: Optional[CalibrationResult] = None
    quality: Optional[QualityResult] = None
    consistency: Optional[ConsistencyResult] = None
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary for metadata embedding."""
        return {
            "passed": self.passed,
            "summary": self.summary,
            "validation": {
                "status": self.validation.status.value if self.validation else None,
                "passed": self.validation.passed if self.validation else 0,
                "failed": self.validation.failed if self.validation else 0,
                "warned": self.validation.warned if self.validation else 0,
            },
            "calibration": {
                "ece": self.calibration.ece if self.calibration else None,
                "brier": self.calibration.brier if self.calibration else None,
                "is_calibrated": self.calibration.is_calibrated if self.calibration else None,
            },
            "quality": {
                "overall_score": self.quality.overall_score.value if self.quality else None,
            },
            "consistency": {
                "is_consistent": self.consistency.is_consistent if self.consistency else None,
                "deviation_score": self.consistency.deviation_score if self.consistency else None,
                "contradiction_count": len(self.consistency.contradictions) if self.consistency else 0,
            },
        }


class VerificationOrchestrator:
    """Orchestrates the full verification pipeline.

    Runs validation, calibration, quality assessment, and consistency
    checking on processing results, producing a composite report.

    Example:
        >>> orch = VerificationOrchestrator()
        >>> report = orch.verify(result, history=[], context={})
        >>> print(report.passed, report.summary)
    """

    def __init__(
        self,
        validator: Optional[OutputValidator] = None,
        calibrator: Optional[ConfidenceCalibrator] = None,
        quality_assessor: Optional[QualityAssessor] = None,
        consistency_checker: Optional[ConsistencyChecker] = None,
    ):
        """Initialize orchestrator with optional pre-configured components.

        Args:
            validator: OutputValidator instance.
            calibrator: ConfidenceCalibrator instance.
            quality_assessor: QualityAssessor instance.
            consistency_checker: ConsistencyChecker instance.
        """
        self.validator = validator or OutputValidator()
        self.calibrator = calibrator or ConfidenceCalibrator()
        self.quality_assessor = quality_assessor or QualityAssessor()
        self.consistency_checker = consistency_checker or ConsistencyChecker()

    def verify(
        self,
        result: Any,
        history: Optional[List[Any]] = None,
        context: Optional[Dict] = None,
    ) -> VerificationReport:
        """Run the full verification pipeline on a processing result.

        Pipeline: validate → calibrate → quality → consistency.

        Args:
            result: The processing result to verify (ProcessingResult or similar).
            history: List of previous results for consistency checking.
            context: Optional context dictionary.

        Returns:
            VerificationReport with overall passed/failed and all sub-results.
        """
        if context is None:
            context = {}

        # Extract output and confidence from result
        output = self._extract_output(result)
        confidence = self._extract_confidence(result)

        report = VerificationReport()

        # 1. Validate output
        report.validation = self.validator.validate(output, context)
        logger.debug(
            f"Validation: {report.validation.status.value} "
            f"(passed={report.validation.passed}, "
            f"failed={report.validation.failed}, "
            f"warned={report.validation.warned})"
        )

        # 2. Calibrate confidence
        calib_confidences = [confidence] if confidence is not None else []
        calib_outcomes = [context.get("expected_outcome", 1)] if confidence is not None else []
        report.calibration = self.calibrator.calibrate(calib_confidences, calib_outcomes)
        logger.debug(
            f"Calibration: ece={report.calibration.ece:.4f}, "
            f"brier={report.calibration.brier:.4f}"
        )

        # 3. Assess quality
        report.quality = self.quality_assessor.assess(output, context)
        logger.debug(f"Quality: {report.quality.overall_score.value}")

        # 4. Check consistency
        report.consistency = self.consistency_checker.check(result, history)
        logger.debug(
            f"Consistency: {'consistent' if report.consistency.is_consistent else 'inconsistent'} "
            f"(deviation={report.consistency.deviation_score:.2f})"
        )

        # Determine overall pass/fail
        validation_failed = (
            report.validation.status == ValidationStatus.FAIL
        )
        calibration_failed = not report.calibration.is_calibrated
        quality_failed = report.quality.overall_score in (
            QualityScore.POOR, QualityScore.FAIR
        )
        consistency_failed = not report.consistency.is_consistent

        report.passed = not any([
            validation_failed,
            calibration_failed,
            consistency_failed,
        ])

        # Build summary
        parts = []
        if report.passed:
            parts.append("Verification PASSED")
        else:
            parts.append("Verification FAILED")

        if validation_failed:
            parts.append("validation issues detected")
        if calibration_failed:
            parts.append("confidence miscalibrated")
        if quality_failed:
            parts.append(f"quality is {report.quality.overall_score.value}")
        if consistency_failed:
            parts.append(f"{len(report.consistency.contradictions)} contradictions found")

        report.summary = "; ".join(parts) if len(parts) > 1 else parts[0]

        return report

    def _extract_output(self, result: Any) -> Any:
        """Extract output from a result object."""
        if result is None:
            return None
        if hasattr(result, "output"):
            return result.output
        return result

    def _extract_confidence(self, result: Any) -> Optional[float]:
        """Extract confidence from a result object."""
        if result is None:
            return None
        if hasattr(result, "confidence"):
            return result.confidence
        if isinstance(result, dict):
            return result.get("confidence")
        return None

    def reset(self) -> None:
        """Reset all verification components."""
        self.validator.reset()
