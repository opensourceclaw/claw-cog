"""
Metacognitive Assessment - meta-d' Framework.

Implements Signal Detection Theory (SDT) based metacognitive assessment
as described in Maniscalco & Lau (2012) and "Measuring the Metacognition of AI".
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import logging

from claw_cog.config.defaults import Config

logger = logging.getLogger(__name__)

# Try to import numpy, but provide fallback
try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    logger.warning("numpy not available, using fallback calculations")


@dataclass
class MetacognitiveMetrics:
    """Metacognitive assessment metrics."""

    meta_d_prime: float
    d_prime: float
    m_ratio: float
    type2_roc_auc: float
    sample_size: int


class MetacognitiveAssessment:
    """
    Metacognitive Assessment using meta-d' framework.

    Based on:
    - Maniscalco & Lau (2012): "A signal detection theoretic approach
      for estimating metacognitive sensitivity from confidence ratings"
    - arXiv:2603.29693: "Measuring the Metacognition of AI"

    meta-d' measures Type-2 sensitivity: the ability to distinguish
    correct from incorrect responses using confidence ratings.

    M-ratio = meta-d' / d' measures metacognitive efficiency.
    M-ratio → 1.0 indicates optimal metacognition.
    """

    def __init__(self, config: Config):
        """Initialize assessment."""
        self.config = config

    def compute_metrics(
        self,
        history: List[Any],
        ground_truth: Optional[List[bool]] = None,
    ) -> Dict[str, float]:
        """
        Compute metacognitive metrics.

        Args:
            history: Processing history
            ground_truth: Optional ground truth for correctness

        Returns:
            Dict containing meta-d', d', M-ratio, Type-2 ROC AUC
        """
        if len(history) < self.config.assessment_min_samples:
            return {
                "meta_d_prime": 0.0,
                "d_prime": 0.0,
                "m_ratio": 0.0,
                "type2_roc_auc": 0.5,
                "sample_size": len(history),
                "warning": f"insufficient_data (need {self.config.assessment_min_samples})",
            }

        # Extract confidences and correctness
        confidences = []
        correctness = []

        for i, result in enumerate(history):
            confidences.append(result.confidence)
            # Use ground truth if provided, otherwise assume correct
            if ground_truth and i < len(ground_truth):
                correctness.append(ground_truth[i])
            else:
                # v1.0.0: Assume high confidence = correct
                correctness.append(result.confidence > 0.5)

        # Compute metrics
        d_prime = self._compute_d_prime(confidences, correctness)
        meta_d_prime = self._compute_meta_d_prime(confidences, correctness)
        m_ratio = meta_d_prime / d_prime if d_prime > 0 else 0.0
        type2_roc_auc = self._compute_type2_roc_auc(confidences, correctness)

        return {
            "meta_d_prime": round(meta_d_prime, 4),
            "d_prime": round(d_prime, 4),
            "m_ratio": round(m_ratio, 4),
            "type2_roc_auc": round(type2_roc_auc, 4),
            "sample_size": len(history),
        }

    def _compute_d_prime(self, confidences: List[float], correctness: List[bool]) -> float:
        """
        Compute d' (Type-1 sensitivity).

        Measures how well the system performs the task.
        """
        if not HAS_NUMPY:
            # Fallback calculation
            correct_conf = [c for c, corr in zip(confidences, correctness) if corr]
            incorrect_conf = [c for c, corr in zip(confidences, correctness) if not corr]

            if not correct_conf or not incorrect_conf:
                return 0.0

            mean_diff = sum(correct_conf) / len(correct_conf) - sum(incorrect_conf) / len(
                incorrect_conf
            )
            return abs(mean_diff)

        correct_conf = np.array([c for c, corr in zip(confidences, correctness) if corr])
        incorrect_conf = np.array([c for c, corr in zip(confidences, correctness) if not corr])

        if len(correct_conf) == 0 or len(incorrect_conf) == 0:
            return 0.0

        # Compute d' using SDT formula
        mean_correct = np.mean(correct_conf)
        mean_incorrect = np.mean(incorrect_conf)
        var_correct = np.var(correct_conf)
        var_incorrect = np.var(incorrect_conf)

        std_pooled = np.sqrt((var_correct + var_incorrect) / 2)
        if std_pooled == 0:
            return 0.0

        return float((mean_correct - mean_incorrect) / std_pooled)

    def _compute_meta_d_prime(self, confidences: List[float], correctness: List[bool]) -> float:
        """
        Compute meta-d' (Type-2 sensitivity).

        Measures how well confidence ratings distinguish correct
        from incorrect responses.
        """
        # v1.0.0: Simplified approximation using Type-2 ROC
        type2_roc_auc = self._compute_type2_roc_auc(confidences, correctness)

        # Approximate meta-d' from Type-2 ROC AUC
        # meta-d' ≈ 2 * (Type-2 ROC AUC - 0.5)
        meta_d = 2 * (type2_roc_auc - 0.5)
        return max(0.0, meta_d)

    def _compute_type2_roc_auc(self, confidences: List[float], correctness: List[bool]) -> float:
        """
        Compute Type-2 ROC AUC.

        Area under the ROC curve for confidence-based
        discrimination of correct vs incorrect responses.
        """
        correct_conf = [c for c, corr in zip(confidences, correctness) if corr]
        incorrect_conf = [c for c, corr in zip(confidences, correctness) if not corr]

        if not correct_conf or not incorrect_conf:
            return 0.5  # Chance level

        # Compute AUC: proportion of correct confidences higher than incorrect
        higher_count = 0
        equal_count = 0

        for c in correct_conf:
            for i in incorrect_conf:
                if c > i:
                    higher_count += 1
                elif c == i:
                    equal_count += 1

        total_pairs = len(correct_conf) * len(incorrect_conf)
        if total_pairs == 0:
            return 0.5

        # AUC = (higher + 0.5 * equal) / total
        auc = (higher_count + 0.5 * equal_count) / total_pairs
        return auc

    def compute_significance(
        self, history: List[Any], n_permutations: int = 1000
    ) -> Dict[str, Any]:
        """Compute statistical significance of metacognitive ability.

        Uses permutation test to determine if meta-d' is significantly
        above chance level (meta-d' = 0).

        Args:
            history: Processing history with confidence scores
            n_permutations: Number of permutation iterations

        Returns:
            Dict with p_value, significant flag, and confidence interval
        """
        if len(history) < 10:
            return {"p_value": 1.0, "significant": False, "ci_95": (0.0, 0.0)}

        confidences = [r.confidence for r in history]
        correctness = [getattr(r, "correct", r.confidence > 0.5) for r in history]

        # Observed meta-d'
        observed = self._compute_meta_d_prime(confidences, correctness)

        # Permutation test
        count_exceed = 0
        from random import shuffle

        perm_correctness = list(correctness)

        for _ in range(n_permutations):
            shuffle(perm_correctness)
            perm_meta_d = self._compute_meta_d_prime(confidences, perm_correctness)
            if perm_meta_d >= observed:
                count_exceed += 1

        p_value = (count_exceed + 1) / (n_permutations + 1)

        # 95% CI bootstrap
        ci_low, ci_high = self._bootstrap_ci(confidences, correctness)

        return {
            "observed_meta_d": round(observed, 4),
            "p_value": round(p_value, 4),
            "significant": p_value < 0.05,
            "ci_95": (round(ci_low, 4), round(ci_high, 4)),
            "sample_size": len(history),
        }

    def _bootstrap_ci(
        self, confidences: List[float], correctness: List[bool], n_bootstrap: int = 500
    ) -> tuple:
        """Compute 95% bootstrap confidence interval for meta-d'."""
        from random import choices

        n = len(confidences)
        if n < 5:
            return (0.0, 0.0)

        estimates = []
        indices = list(range(n))
        for _ in range(n_bootstrap):
            sampled = choices(indices, k=n)
            bs_conf = [confidences[i] for i in sampled]
            bs_corr = [correctness[i] for i in sampled]
            estimates.append(self._compute_meta_d_prime(bs_conf, bs_corr))

        estimates.sort()
        ci_low = estimates[int(0.025 * len(estimates))]
        ci_high = estimates[int(0.975 * len(estimates))]
        return (ci_low, ci_high)
