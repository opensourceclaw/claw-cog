"""Confidence calibration for verification layer."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
import logging

from claw_cog.consciousness.verification.metrics.calibration import (
    expected_calibration_error,
    brier_score,
    accuracy_at_confidence,
)

logger = logging.getLogger(__name__)


class CalibrationBin(Enum):
    """Confidence bins for calibration analysis."""

    LOW = "low"        # < 0.5
    MEDIUM = "medium"  # 0.5 – 0.8
    HIGH = "high"       # > 0.8


@dataclass
class CalibrationResult:
    """Result of confidence calibration analysis.

    Attributes:
        ece: Expected Calibration Error.
        brier: Brier score.
        num_samples: Number of samples evaluated.
        is_calibrated: Whether the predictions are well-calibrated (ECE < threshold).
        calibration_status: Descriptive status string.
        per_bin: Accuracy breakdown by confidence bin.
    """

    ece: float = 0.0
    brier: float = 0.0
    num_samples: int = 0
    is_calibrated: bool = True
    calibration_status: str = "no_data"
    per_bin: Dict[str, float] = field(default_factory=dict)


class ConfidenceCalibrator:
    """Evaluates confidence calibration quality.

    Computes ECE, Brier score, and per-bin accuracy to determine
    whether an agent's confidence estimates are well-calibrated.

    Example:
        >>> calibrator = ConfidenceCalibrator(ece_threshold=0.1)
        >>> result = calibrator.calibrate(
        ...     confidences=[0.9, 0.7, 0.3, 0.8],
        ...     outcomes=[1, 1, 0, 1],
        ... )
        >>> print(result.is_calibrated)
    """

    def __init__(self, ece_threshold: float = 0.1, num_bins: int = 10):
        """Initialize calibrator.

        Args:
            ece_threshold: Threshold below which calibration is considered good.
            num_bins: Number of bins for ECE computation.
        """
        self.ece_threshold = ece_threshold
        self.num_bins = num_bins

    def calibrate(self, confidences: List[float],
                  outcomes: List[int]) -> CalibrationResult:
        """Run calibration analysis on confidence-outcome pairs.

        Args:
            confidences: List of confidence values (0.0–1.0).
            outcomes: List of binary outcomes (1 = correct, 0 = incorrect).

        Returns:
            CalibrationResult with ECE, Brier, and status.

        Raises:
            ValueError: If confidences and outcomes have differing lengths.
        """
        if len(confidences) != len(outcomes):
            raise ValueError(
                f"confidences and outcomes must have the same length "
                f"({len(confidences)} vs {len(outcomes)})"
            )

        num_samples = len(confidences)
        if num_samples == 0:
            return CalibrationResult(
                ece=0.0,
                brier=0.0,
                num_samples=0,
                is_calibrated=True,
                calibration_status="no_data",
            )

        ece = expected_calibration_error(confidences, outcomes, self.num_bins)
        brier = brier_score(confidences, outcomes)
        per_bin = accuracy_at_confidence(confidences, outcomes)

        is_calibrated = ece <= self.ece_threshold

        if is_calibrated:
            status = "well_calibrated"
        elif ece <= self.ece_threshold * 2:
            status = "moderately_miscalibrated"
        else:
            status = "poorly_calibrated"

        return CalibrationResult(
            ece=ece,
            brier=brier,
            num_samples=num_samples,
            is_calibrated=is_calibrated,
            calibration_status=status,
            per_bin=per_bin,
        )
