"""Tests for claw_cog.consciousness.verification.calibrator."""

import pytest
from claw_cog.consciousness.verification.calibrator import (
    ConfidenceCalibrator,
    CalibrationResult,
)


@pytest.fixture
def calibrator():
    return ConfidenceCalibrator(ece_threshold=0.1, num_bins=10)


class TestConfidenceCalibrator:
    def test_perfect_calibration(self, calibrator):
        confidences = [0.8, 0.9, 0.7, 0.85]
        outcomes = [1, 1, 1, 1]
        result = calibrator.calibrate(confidences, outcomes)
        assert result.num_samples == 4
        assert result.brier >= 0.0
        assert "low" in result.per_bin or "medium" in result.per_bin or "high" in result.per_bin

    def test_over_confident(self, calibrator):
        confidences = [0.95, 0.95, 0.95, 0.95]
        outcomes = [0, 0, 0, 0]
        result = calibrator.calibrate(confidences, outcomes)
        assert not result.is_calibrated
        assert result.ece > 0.1

    def test_under_confident(self, calibrator):
        confidences = [0.1, 0.1, 0.1, 0.1]
        outcomes = [1, 1, 1, 1]
        result = calibrator.calibrate(confidences, outcomes)
        assert not result.is_calibrated

    def test_empty_calibration(self, calibrator):
        result = calibrator.calibrate([], [])
        assert result.num_samples == 0
        assert result.is_calibrated
        assert result.calibration_status == "no_data"

    def test_mismatched_lengths(self, calibrator):
        with pytest.raises(ValueError):
            calibrator.calibrate([0.5], [1, 0])

    def test_mixed_confidences(self, calibrator):
        confidences = [0.95, 0.9, 0.2, 0.1]
        outcomes = [1, 1, 0, 0]
        result = calibrator.calibrate(confidences, outcomes)
        assert result.ece >= 0.0

    def test_ece_threshold_boundary(self):
        c = ConfidenceCalibrator(ece_threshold=0.2)
        confidences = [0.8, 0.9, 0.3, 0.2]
        outcomes = [1, 1, 0, 0]
        result = c.calibrate(confidences, outcomes)
        assert isinstance(result.is_calibrated, bool)

    def test_calibration_status_well(self):
        calibrator = ConfidenceCalibrator(ece_threshold=0.5)
        confidences = [0.7, 0.8]
        outcomes = [1, 1]
        result = calibrator.calibrate(confidences, outcomes)
        assert result.calibration_status == "well_calibrated"

    def test_calibration_status_poorly(self):
        calibrator = ConfidenceCalibrator(ece_threshold=0.05)
        confidences = [0.95, 0.95]
        outcomes = [0, 0]
        result = calibrator.calibrate(confidences, outcomes)
        assert result.calibration_status == "poorly_calibrated"

    def test_per_bin_accuracy(self, calibrator):
        confidences = [0.3, 0.3, 0.6, 0.6, 0.9, 0.9]
        outcomes = [0, 0, 1, 1, 1, 1]
        result = calibrator.calibrate(confidences, outcomes)
        assert result.per_bin["low"] == 0.0
        assert result.per_bin["medium"] == 1.0
        assert result.per_bin["high"] == 1.0
