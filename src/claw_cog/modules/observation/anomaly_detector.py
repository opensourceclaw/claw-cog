"""AnomalyDetector — detects anomalies by comparing observations against baselines."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from .types import Anomaly, SeverityLevel


class AnomalyDetector:
    """
    Detects anomalies in observations.

    Classifies deviation severity using configurable thresholds:
    - deviation < low_threshold -> LOW
    - deviation < medium_threshold -> MEDIUM
    - deviation < high_threshold -> HIGH
    - deviation >= high_threshold -> CRITICAL
    """

    def __init__(
        self,
        low_threshold: float = 0.1,
        medium_threshold: float = 0.3,
        high_threshold: float = 0.5,
    ):
        self.low_threshold = low_threshold
        self.medium_threshold = medium_threshold
        self.high_threshold = high_threshold
        self._stats = {"anomalies_detected": 0}

    def detect(
        self,
        observations: List,
        baselines: Dict[str, Dict[str, float]],
    ) -> List[Anomaly]:
        """
        Detect anomalies by comparing observation values to baselines.

        Args:
            observations: List of Observation objects
            baselines: Nested dict of layer -> metric -> expected_value

        Returns:
            List of Anomaly objects for significant deviations
        """
        anomalies = []
        now = datetime.now(timezone.utc).isoformat()

        for obs in observations:
            expected = self._get_expected(obs.layer, obs.metric, baselines)
            deviation = abs(obs.value - expected)
            severity = self._classify_severity(deviation)

            if deviation > 0:
                anomaly = Anomaly(
                    anomaly_id=f"anom-{uuid.uuid4().hex[:12]}",
                    layer=obs.layer,
                    metric=obs.metric,
                    observed_value=obs.value,
                    expected_value=expected,
                    deviation=deviation,
                    severity=severity,
                    timestamp=now,
                    description=f"[{severity.value.upper()}] {obs.layer}.{obs.metric} deviated by {deviation:.3f} (observed={obs.value:.3f}, expected={expected:.3f})",
                )
                anomalies.append(anomaly)
                self._stats["anomalies_detected"] += 1

        return anomalies

    def get_statistics(self) -> Dict[str, Any]:
        return {**self._stats}

    def clear(self):
        """Reset anomaly statistics."""
        self._stats = {"anomalies_detected": 0}

    def _classify_severity(self, deviation: float) -> SeverityLevel:
        if deviation < self.medium_threshold:
            if deviation < self.low_threshold:
                return SeverityLevel.LOW
            return SeverityLevel.MEDIUM
        if deviation < self.high_threshold:
            return SeverityLevel.HIGH
        return SeverityLevel.CRITICAL

    @staticmethod
    def _get_expected(layer: str, metric: str, baselines: Dict[str, Dict[str, float]]) -> float:
        return baselines.get(layer, {}).get(metric, 0.5)


__all__ = ["AnomalyDetector"]
