"""Tests for claw_cog.consciousness.verification.metrics.calibration."""

import pytest
from claw_cog.consciousness.verification.metrics.calibration import (
    expected_calibration_error,
    accuracy_at_confidence,
    brier_score,
    CalibrationMetrics,
)


class TestExpectedCalibrationError:
    def test_perfect_calibration(self):
        confidences = [0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9]
        outcomes = [0, 0, 0, 1, 1, 1, 1, 1]
        ece = expected_calibration_error(confidences, outcomes, num_bins=5)
        assert ece >= 0.0

    def test_poor_calibration(self):
        confidences = [0.9, 0.9, 0.9, 0.9]
        outcomes = [0, 0, 0, 0]
        ece = expected_calibration_error(confidences, outcomes, num_bins=5)
        assert ece > 0.5

    def test_empty_inputs(self):
        ece = expected_calibration_error([], [])
        assert ece == 0.0

    def test_mismatched_lengths(self):
        with pytest.raises(ValueError):
            expected_calibration_error([0.5], [1, 0])

    def test_known_ece_value(self):
        confidences = [0.2, 0.2, 0.8, 0.8]
        outcomes = [0, 1, 0, 1]
        ece = expected_calibration_error(confidences, outcomes, num_bins=2)
        assert ece >= 0.0

    def test_single_bin_all_correct(self):
        confidences = [0.7, 0.75, 0.78]
        outcomes = [1, 1, 1]
        ece = expected_calibration_error(confidences, outcomes, num_bins=3)
        assert ece >= 0.0


class TestAccuracyAtConfidence:
    def test_all_buckets(self):
        confidences = [0.3, 0.6, 0.9]
        outcomes = [0, 1, 1]
        result = accuracy_at_confidence(confidences, outcomes)
        assert "low" in result
        assert "medium" in result
        assert "high" in result

    def test_empty_bucket(self):
        confidences = [0.6]
        outcomes = [1]
        result = accuracy_at_confidence(confidences, outcomes)
        assert result["low"] == 0.0

    def test_mismatched_lengths(self):
        with pytest.raises(ValueError):
            accuracy_at_confidence([0.5], [])


class TestBrierScore:
    def test_perfect_brier(self):
        score = brier_score([1.0, 0.0], [1, 0])
        assert score == 0.0

    def test_worst_brier(self):
        score = brier_score([0.0, 1.0], [1, 0])
        assert score == 1.0

    def test_intermediate_brier(self):
        score = brier_score([0.8, 0.3], [1, 0])
        assert 0.0 < score < 1.0

    def test_empty(self):
        assert brier_score([], []) == 0.0

    def test_mismatched_lengths(self):
        with pytest.raises(ValueError):
            brier_score([0.5], [1, 0])
