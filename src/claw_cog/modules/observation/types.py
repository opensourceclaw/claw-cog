"""Observation type definitions: Observation, Anomaly, and SeverityLevel."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict


class SeverityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Observation:
    """A single observation of a layer's metric at a point in time."""

    observation_id: str
    layer: str
    metric: str
    value: float
    baseline: float = 0.0
    timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "observation_id": self.observation_id,
            "layer": self.layer,
            "metric": self.metric,
            "value": self.value,
            "baseline": self.baseline,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


@dataclass
class Anomaly:
    """An anomaly detected when a metric deviates from its baseline."""

    anomaly_id: str
    layer: str
    metric: str
    observed_value: float
    expected_value: float
    deviation: float
    severity: SeverityLevel
    timestamp: str = ""
    description: str = ""

    def to_dict(self) -> dict:
        return {
            "anomaly_id": self.anomaly_id,
            "layer": self.layer,
            "metric": self.metric,
            "observed_value": self.observed_value,
            "expected_value": self.expected_value,
            "deviation": self.deviation,
            "severity": self.severity.value,
            "timestamp": self.timestamp,
            "description": self.description,
        }


__all__ = [
    "Observation",
    "Anomaly",
    "SeverityLevel",
]
