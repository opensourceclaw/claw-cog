"""Verification layer for claw-cog.

Provides output validation, confidence calibration, quality assessment,
and consistency checking for conscious processing results.
"""

from .validator import OutputValidator, ValidationResult, ValidationStatus
from .calibrator import ConfidenceCalibrator, CalibrationResult, CalibrationBin
from .quality import QualityAssessor, QualityResult, QualityScore
from .consistency import ConsistencyChecker, ConsistencyResult
from .orchestrator import VerificationOrchestrator, VerificationReport

__all__ = [
    "CalibrationBin",
    "CalibrationResult",
    "ConfidenceCalibrator",
    "ConsistencyChecker",
    "ConsistencyResult",
    "OutputValidator",
    "QualityAssessor",
    "QualityResult",
    "QualityScore",
    "ValidationResult",
    "ValidationStatus",
    "VerificationOrchestrator",
    "VerificationReport",
]
