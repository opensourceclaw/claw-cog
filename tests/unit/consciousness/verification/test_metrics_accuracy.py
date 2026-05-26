"""Tests for claw_cog.consciousness.verification.metrics.accuracy."""

import pytest
from claw_cog.consciousness.verification.metrics.accuracy import (
    compute_accuracy,
    AccuracyMetrics,
)


class TestComputeAccuracy:
    def test_perfect_accuracy(self):
        predictions = ["a", "b", "c", "d"]
        ground_truth = ["a", "b", "c", "d"]
        result = compute_accuracy(predictions, ground_truth)
        assert result.accuracy == 1.0
        assert result.correct == 4
        assert result.total == 4

    def test_half_accuracy(self):
        predictions = ["a", "b", "c", "d"]
        ground_truth = ["a", "b", "x", "y"]
        result = compute_accuracy(predictions, ground_truth)
        assert result.accuracy == 0.5
        assert result.correct == 2

    def test_empty_lists(self):
        result = compute_accuracy([], [])
        assert result.total == 0
        assert result.accuracy == 0.0
        assert result.per_class == {}

    def test_per_class_accuracy(self):
        predictions = ["a", "a", "b", "b", "c"]
        ground_truth = ["a", "a", "b", "x", "c"]
        result = compute_accuracy(predictions, ground_truth)
        assert result.per_class["a"] == 1.0
        # Class "b" has one ground truth sample which matches prediction[2]
        assert result.per_class["b"] == 1.0
        assert result.per_class["x"] == 0.0
        assert result.per_class["c"] == 1.0

    def test_mismatched_lengths(self):
        with pytest.raises(ValueError):
            compute_accuracy(["a"], ["a", "b"])

    def test_all_wrong(self):
        predictions = ["a", "b"]
        ground_truth = ["x", "y"]
        result = compute_accuracy(predictions, ground_truth)
        assert result.accuracy == 0.0
        assert result.correct == 0
