"""SelfMonitor — tracks layer metrics, establishes baselines, computes trends."""

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional


Trend = Literal["improving", "stable", "declining"]


class SelfMonitor:
    """
    Monitors internal layer states over time.

    Tracks per-layer, per-metric history to:
    - Establish rolling baselines (mean of stored values)
    - Compute trends (comparing recent vs. baseline)
    - Support anomaly detection with expected values
    """

    def __init__(self, history_size: int = 100):
        self.history_size = history_size
        self._history: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
        self._stats = {"observations_tracked": 0}

    def track(
        self, layer: str, metric: str, value: float, timestamp: Optional[str] = None
    ):
        """Record a metric observation for a layer."""
        timestamp or datetime.now(timezone.utc).isoformat()
        values = self._history[layer][metric]
        values.append(value)
        if len(values) > self.history_size:
            values.pop(0)
        self._stats["observations_tracked"] += 1

    def get_baseline(self, layer: str, metric: str) -> float:
        """Get the baseline (mean) for a layer metric. Returns 0.5 if no data."""
        values = self._history.get(layer, {}).get(metric, [])
        if not values:
            return 0.5
        return sum(values) / len(values)

    def get_trend(self, layer: str, metric: str) -> Trend:
        """
        Compute the trend direction for a layer metric.

        Compares the average of the last N/2 values against the overall baseline.
        Returns "improving", "stable", or "declining".
        """
        values = self._history.get(layer, {}).get(metric, [])
        if len(values) < 4:
            return "stable"

        baseline = self.get_baseline(layer, metric)
        half = max(1, len(values) // 2)
        recent = values[-half:]
        recent_avg = sum(recent) / len(recent)

        ratio = recent_avg / baseline if baseline > 0 else 1.0
        if ratio > 1.1:
            return "improving"
        elif ratio < 0.9:
            return "declining"
        return "stable"

    def get_statistics(self) -> Dict[str, Any]:
        """Return monitor statistics."""
        layer_count = len(self._history)
        metric_count = sum(len(metrics) for metrics in self._history.values())
        return {
            **self._stats,
            "layers_tracked": layer_count,
            "metrics_tracked": metric_count,
        }

    def clear(self):
        """Clear all tracked history and reset statistics."""
        self._history.clear()
        self._stats = {"observations_tracked": 0}


__all__ = ["SelfMonitor", "Trend"]
