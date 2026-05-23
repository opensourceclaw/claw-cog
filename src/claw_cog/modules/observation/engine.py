"""ObservationEngine — O layer of ETCLOVG architecture. Observes all layer states."""

import uuid
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

from .types import Observation, Anomaly
from .self_monitor import SelfMonitor
from .anomaly_detector import AnomalyDetector

logger = logging.getLogger(__name__)


class ObservationEngine:
    """
    Observation Engine — O layer of ETCLOVG architecture.

    Observes state snapshots from all layers (C0, C1, C2, volition, temporal)
    and detects anomalies by comparing against historical baselines.

    Uses the ClawMemBridge for episodic memory of observations.
    """

    def __init__(
        self,
        monitor: SelfMonitor,
        detector: AnomalyDetector,
        memory=None,
    ):
        self.monitor = monitor
        self.detector = detector
        self.memory = memory
        self._stats = {"observations_made": 0, "anomalies_detected": 0}

    def observe(self, layer_states: Dict[str, Any]) -> List[Observation]:
        """
        Observe current layer states and produce observations.

        Args:
            layer_states: Dict mapping layer name to Dict of metric->value.
                Expected keys: "c0", "c1", "c2", "memory", "volition", "temporal"

        Returns:
            List of Observation objects, one per metric.
        """
        observations = []
        now = datetime.now(timezone.utc).isoformat()

        for layer, metrics in layer_states.items():
            if not isinstance(metrics, dict):
                continue
            for metric, value in metrics.items():
                if not isinstance(value, (int, float)):
                    continue
                baseline = self.monitor.get_baseline(layer, metric)
                obs = Observation(
                    observation_id=f"obs-{uuid.uuid4().hex[:12]}",
                    layer=layer,
                    metric=metric,
                    value=float(value),
                    baseline=baseline,
                    timestamp=now,
                )
                observations.append(obs)
                self.monitor.track(layer, metric, float(value), timestamp=now)

        self._stats["observations_made"] += len(observations)
        return observations

    def detect_anomalies(self, observations: List[Observation]) -> List[Anomaly]:
        """
        Detect anomalies across all observations.

        Builds baseline map from SelfMonitor and delegates to AnomalyDetector.
        """
        baselines: Dict[str, Dict[str, float]] = {}
        for obs in observations:
            baselines.setdefault(obs.layer, {})
            baselines[obs.layer][obs.metric] = self.monitor.get_baseline(
                obs.layer, obs.metric
            )

        anomalies = self.detector.detect(observations, baselines)
        self._stats["anomalies_detected"] += len(anomalies)

        # Store anomalies in memory bridge for episodic recall
        if anomalies and self.memory:
            for anomaly in anomalies:
                try:
                    self.memory.store(
                        memory_type="experience",
                        content=anomaly.description,
                        metadata={
                            "layer": anomaly.layer,
                            "metric": anomaly.metric,
                            "severity": anomaly.severity.value,
                            "deviation": anomaly.deviation,
                        },
                    )
                except Exception:
                    logger.debug("Failed to store anomaly in memory bridge", exc_info=True)

        return anomalies

    def get_statistics(self) -> Dict[str, Any]:
        """Return engine statistics including monitor and detector stats."""
        return {
            **self._stats,
            "monitor": self.monitor.get_statistics(),
            "detector": self.detector.get_statistics(),
        }

    def clear(self):
        """Clear all observation state."""
        self.monitor.clear()
        self.detector.clear()
        self._stats = {"observations_made": 0, "anomalies_detected": 0}


__all__ = ["ObservationEngine"]
