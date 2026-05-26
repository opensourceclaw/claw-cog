"""Consciousness package for claw-cog.

Contains the verification layer for validating and calibrating
conscious processing results.
"""

from .verification import (
    CalibrationBin,
    CalibrationResult,
    ConfidenceCalibrator,
    ConsistencyChecker,
    ConsistencyResult,
    OutputValidator,
    QualityAssessor,
    QualityResult,
    QualityScore,
    ValidationResult,
    ValidationStatus,
    VerificationOrchestrator,
    VerificationReport,
)

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
