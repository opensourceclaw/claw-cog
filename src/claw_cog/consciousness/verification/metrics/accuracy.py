"""Accuracy metrics for verification."""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AccuracyMetrics:
    """Container for accuracy-related metrics.

    Attributes:
        total: Total number of samples.
        correct: Number of correct predictions.
        accuracy: Overall accuracy (correct / total).
        per_class: Per-class accuracy breakdown (class label -> accuracy).
    """

    total: int = 0
    correct: int = 0
    accuracy: float = 0.0
    per_class: Dict[str, float] = field(default_factory=dict)


def compute_accuracy(predictions: List[Any], ground_truth: List[Any]) -> AccuracyMetrics:
    """Compute accuracy metrics for a set of predictions.

    Args:
        predictions: List of predicted values.
        ground_truth: List of expected (ground truth) values.

    Returns:
        AccuracyMetrics with overall and per-class accuracy.

    Raises:
        ValueError: If predictions and ground_truth have differing lengths.
    """
    if len(predictions) != len(ground_truth):
        raise ValueError(
            f"predictions and ground_truth must have the same length "
            f"({len(predictions)} vs {len(ground_truth)})"
        )

    total = len(predictions)
    if total == 0:
        return AccuracyMetrics(total=0, correct=0, accuracy=0.0)

    correct = sum(1 for p, g in zip(predictions, ground_truth) if p == g)

    # Per-class accuracy
    per_class: Dict[str, float] = {}
    class_counts: Dict[str, int] = {}
    class_correct: Dict[str, int] = {}

    for p, g in zip(predictions, ground_truth):
        key = str(g)
        class_counts[key] = class_counts.get(key, 0) + 1
        if p == g:
            class_correct[key] = class_correct.get(key, 0) + 1

    for key, count in class_counts.items():
        per_class[key] = class_correct.get(key, 0) / count if count > 0 else 0.0

    return AccuracyMetrics(
        total=total,
        correct=correct,
        accuracy=correct / total,
        per_class=per_class,
    )
