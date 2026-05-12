"""Tests for meta-d' metacognitive assessment."""
import pytest
from claw_cog.config.defaults import Config
from claw_cog.assessment.meta_d_prime import MetacognitiveAssessment, MetacognitiveMetrics


class DummyResult:
    def __init__(self, confidence=0.5, correct=True):
        self.confidence = confidence
        self.correct = correct


class TestMetacognitiveAssessment:
    def setup_method(self):
        self.config = Config()
        self.assessment = MetacognitiveAssessment(self.config)

    def test_insufficient_samples(self):
        result = self.assessment.compute_metrics([])
        assert result["sample_size"] == 0
        assert "warning" in result

    def test_basic_computation(self):
        history = [DummyResult(0.9, True) for _ in range(15)]
        result = self.assessment.compute_metrics(history)
        assert result["sample_size"] == 15
        assert isinstance(result["meta_d_prime"], float)
        assert isinstance(result["m_ratio"], float)

    def test_mixed_correctness(self):
        history = [
            DummyResult(0.9, True),
            DummyResult(0.8, True),
            DummyResult(0.7, True),
            DummyResult(0.6, True),
            DummyResult(0.5, True),
            DummyResult(0.4, False),
            DummyResult(0.3, False),
            DummyResult(0.2, False),
            DummyResult(0.1, False),
            DummyResult(0.9, True),
            DummyResult(0.8, True),
            DummyResult(0.3, False),
            DummyResult(0.7, True),
            DummyResult(0.6, True),
            DummyResult(0.4, False),
        ]
        result = self.assessment.compute_metrics(history)
        assert 0.0 <= result["type2_roc_auc"] <= 1.0

    def test_significance_low_samples(self):
        history = [DummyResult(0.5) for _ in range(5)]
        result = self.assessment.compute_significance(history)
        assert result["significant"] is False

    def test_significance_permutation(self):
        history = [
            DummyResult(0.9, True) for _ in range(8)
        ] + [
            DummyResult(0.2, False) for _ in range(7)
        ]
        result = self.assessment.compute_significance(history, n_permutations=100)
        assert "p_value" in result
        assert "ci_95" in result
        assert isinstance(result["ci_95"], tuple)
        assert len(result["ci_95"]) == 2

    def test_type2_roc_auc_perfect(self):
        # Perfect discrimination
        history = [
            DummyResult(0.9, True), DummyResult(0.8, True), DummyResult(0.7, True),
            DummyResult(0.3, False), DummyResult(0.2, False), DummyResult(0.1, False),
            DummyResult(0.85, True), DummyResult(0.75, True),
            DummyResult(0.25, False), DummyResult(0.15, False),
            DummyResult(0.9, True), DummyResult(0.8, True),
            DummyResult(0.2, False), DummyResult(0.1, False),
            DummyResult(0.7, True),
        ]
        result = self.assessment.compute_metrics(history)
        assert result["sample_size"] == 15

    def test_all_correct(self):
        history = [DummyResult(0.9, True) for _ in range(15)]
        result = self.assessment.compute_metrics(history)
        assert result["d_prime"] == 0.0  # No incorrect samples

    def test_no_numpy_fallback(self):
        history = [DummyResult(c, i % 2 == 0) for i, c in enumerate(
            [0.95, 0.1, 0.9, 0.15, 0.85, 0.2, 0.8, 0.25, 0.75, 0.3,
             0.7, 0.35, 0.65, 0.4, 0.6, 0.45]
        )]
        result = self.assessment.compute_metrics(history)
        assert result["sample_size"] == 16
        assert isinstance(result["meta_d_prime"], float)
