"""Calibration metrics for confidence evaluation."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class CalibrationMetrics:
    """Container for calibration-related metrics.

    Attributes:
        ece: Expected Calibration Error.
        brier: Brier score (mean squared error of confidences).
        num_samples: Number of samples evaluated.
    """

    ece: float = 0.0
    brier: float = 0.0
    num_samples: int = 0


def expected_calibration_error(
    confidences: List[float],
    outcomes: List[int],
    num_bins: int = 10,
) -> float:
    """Compute Expected Calibration Error (ECE).

    Partitions predictions into equally-spaced bins by confidence,
    then computes the weighted average of |accuracy - confidence| per bin.

    Args:
        confidences: List of predicted confidence values (0.0–1.0).
        outcomes: List of binary outcomes (0 or 1, 1 = correct).
        num_bins: Number of confidence bins (default 10).

    Returns:
        ECE value (lower is better calibrated).

    Raises:
        ValueError: If confidences and outcomes lengths differ.
    """
    if len(confidences) != len(outcomes):
        raise ValueError(
            f"confidences and outcomes must have the same length "
            f"({len(confidences)} vs {len(outcomes)})"
        )

    n = len(confidences)
    if n == 0:
        return 0.0

    bin_size = 1.0 / num_bins
    ece = 0.0

    for i in range(num_bins):
        lower = i * bin_size
        upper = (i + 1) * bin_size
        # include upper bound in the last bin
        if i == num_bins - 1:
            mask = [(lower <= c <= upper) for c in confidences]
        else:
            mask = [(lower <= c < upper) for c in confidences]

        bin_indices = [j for j, m in enumerate(mask) if m]
        if not bin_indices:
            continue

        bin_confidences = [confidences[j] for j in bin_indices]
        bin_outcomes = [outcomes[j] for j in bin_indices]

        avg_confidence = sum(bin_confidences) / len(bin_confidences)
        avg_accuracy = sum(bin_outcomes) / len(bin_outcomes)

        ece += (len(bin_indices) / n) * abs(avg_accuracy - avg_confidence)

    return ece


def accuracy_at_confidence(
    confidences: List[float],
    outcomes: List[int],
) -> Dict[str, float]:
    """Compute accuracy at different confidence levels.

    Bucket predictions into: low (<0.5), medium (0.5-0.8), high (>0.8).

    Args:
        confidences: List of predicted confidence values.
        outcomes: List of binary outcomes.

    Returns:
        Dict with keys 'low', 'medium', 'high' mapping to accuracy values.
    """
    if len(confidences) != len(outcomes):
        raise ValueError("confidences and outcomes must have the same length")

    buckets: Dict[str, List[int]] = {"low": [], "medium": [], "high": []}

    for conf, out in zip(confidences, outcomes):
        if conf < 0.5:
            buckets["low"].append(out)
        elif conf <= 0.8:
            buckets["medium"].append(out)
        else:
            buckets["high"].append(out)

    return {key: sum(vals) / len(vals) if vals else 0.0 for key, vals in buckets.items()}


def brier_score(
    confidences: List[float],
    outcomes: List[int],
) -> float:
    """Compute Brier score (mean squared error of probabilistic predictions).

    Brier = (1/N) * Σ(p_i - o_i)²

    Args:
        confidences: List of predicted probabilities.
        outcomes: List of binary outcomes (0 or 1).

    Returns:
        Brier score (lower is better).
    """
    if len(confidences) != len(outcomes):
        raise ValueError("confidences and outcomes must have the same length")
    if len(confidences) == 0:
        return 0.0

    n = len(confidences)
    return sum((c - o) ** 2 for c, o in zip(confidences, outcomes)) / n
