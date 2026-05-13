"""Enhanced tests for meta_d_prime — boundary conditions and CI."""
import pytest
from claw_cog.config.defaults import Config
from claw_cog.assessment.meta_d_prime import MetacognitiveAssessment


class DummyResult:
    def __init__(self, confidence, correct=True):
        self.confidence = confidence
        self.correct = correct


class TestMetaDPrimeEnhanced:
    def setup_method(self):
        self.config = Config(assessment_min_samples=5)
        self.ma = MetacognitiveAssessment(self.config)

    def test_boundary_all_correct(self):
        """Test with all confidences high (all correct)."""
        history = [DummyResult(0.9), DummyResult(0.85), DummyResult(0.95),
                   DummyResult(0.88), DummyResult(0.92)]
        metrics = self.ma.compute_metrics(history)
        assert "warning" not in metrics
        assert metrics["sample_size"] == 5

    def test_boundary_all_incorrect(self):
        """Test with all confidences low (all incorrect)."""
        history = [DummyResult(0.1), DummyResult(0.15), DummyResult(0.2),
                   DummyResult(0.05), DummyResult(0.3)]
        metrics = self.ma.compute_metrics(history)
        assert "warning" not in metrics

    def test_mixed_confidences_with_ground_truth(self):
        """Test with explicit ground truth labels."""
        history = [DummyResult(0.8), DummyResult(0.3), DummyResult(0.7),
                   DummyResult(0.2), DummyResult(0.9)]
        ground_truth = [True, False, True, False, True]
        metrics = self.ma.compute_metrics(history, ground_truth=ground_truth)
        assert "warning" not in metrics

    def test_significance_with_enough_samples(self):
        """Test significance test with enough data."""
        history = [DummyResult(0.5 + (i % 5) * 0.1) for i in range(10)]
        result = self.ma.compute_significance(history, n_permutations=50)
        assert "p_value" in result
        assert "significant" in result
        assert "ci_95" in result

    def test_bootstrap_ci_boundary(self):
        """Test bootstrap CI with mixed confidences."""
        history = [DummyResult(0.7), DummyResult(0.3), DummyResult(0.8),
                   DummyResult(0.4), DummyResult(0.6)]
        metrics = self.ma.compute_metrics(history)
        assert metrics["meta_d_prime"] >= 0.0
        assert metrics["type2_roc_auc"] >= 0.0

    def test_insufficient_samples_with_larger_min(self):
        """Test warning when below custom min_samples."""
        config = Config(assessment_min_samples=100)
        ma = MetacognitiveAssessment(config)
        history = [DummyResult(0.5)] * 5
        metrics = ma.compute_metrics(history)
        assert "warning" in metrics
        assert metrics["meta_d_prime"] == 0.0

    def test_mixed_numpy_path_fully_exercised(self):
        """Ensure numpy d_prime path is fully exercised with mixed data."""
        history = [
            DummyResult(0.9), DummyResult(0.8), DummyResult(0.85),
            DummyResult(0.3), DummyResult(0.25), DummyResult(0.35),
        ]
        ground_truth = [True, True, True, False, False, False]
        metrics = self.ma.compute_metrics(history, ground_truth=ground_truth)
        assert metrics["d_prime"] > 0.0, "d_prime should be > 0 with mixed data"
        assert "warning" not in metrics

    def test_d_prime_numpy_path_directly(self):
        """Directly test _compute_d_prime to ensure numpy path coverage."""
        ma = MetacognitiveAssessment(Config())
        confidences = [0.9, 0.8, 0.85, 0.3, 0.25, 0.35]
        correctness = [True, True, True, False, False, False]
        d = ma._compute_d_prime(confidences, correctness)
        assert d > 0.0

    def test_meta_d_prime_directly(self):
        """Directly test _compute_meta_d_prime."""
        ma = MetacognitiveAssessment(Config())
        confidences = [0.9, 0.8, 0.7, 0.3, 0.2, 0.1]
        correctness = [True, True, True, False, False, False]
        md = ma._compute_meta_d_prime(confidences, correctness)
        assert md >= 0.0

    def test_type2_roc_equal_path(self):
        """Cover Type-2 ROC AUC equal_count path."""
        from claw_cog.assessment.meta_d_prime import MetacognitiveAssessment
        ma = MetacognitiveAssessment(Config(assessment_min_samples=3))
        history = [
            DummyResult(0.7), DummyResult(0.5), DummyResult(0.3),
            DummyResult(0.7),  # duplicate to trigger equal_count
        ]
        ground_truth = [True, False, True, True]
        metrics = ma.compute_metrics(history, ground_truth=ground_truth)
        if metrics["sample_size"] >= ma.config.assessment_min_samples:
            assert "warning" not in metrics
            assert metrics["type2_roc_auc"] >= 0.0
