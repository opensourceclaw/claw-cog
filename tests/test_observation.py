"""Tests for Observation layer (v1.8.0): ObservationEngine, SelfMonitor, AnomalyDetector."""

import pytest
from unittest.mock import Mock

from claw_cog.modules.observation.types import (
    Observation, Anomaly, SeverityLevel,
)
from claw_cog.modules.observation.self_monitor import SelfMonitor
from claw_cog.modules.observation.anomaly_detector import AnomalyDetector
from claw_cog.modules.observation.engine import ObservationEngine


class TestObservation:
    def test_default_creation(self):
        obs = Observation(
            observation_id="o1",
            layer="c1",
            metric="confidence",
            value=0.85,
        )
        assert obs.observation_id == "o1"
        assert obs.layer == "c1"
        assert obs.metric == "confidence"
        assert obs.value == 0.85
        assert obs.baseline == 0.0

    def test_to_dict(self):
        obs = Observation(
            observation_id="o2",
            layer="c2",
            metric="confidence_estimate",
            value=0.6,
            baseline=0.5,
            timestamp="2025-06-01T00:00:00",
            metadata={"source": "test"},
        )
        d = obs.to_dict()
        assert d["observation_id"] == "o2"
        assert d["layer"] == "c2"
        assert d["metric"] == "confidence_estimate"
        assert d["value"] == 0.6
        assert d["baseline"] == 0.5
        assert d["timestamp"] == "2025-06-01T00:00:00"


class TestAnomaly:
    def test_default_creation(self):
        a = Anomaly(
            anomaly_id="a1",
            layer="c2",
            metric="confidence",
            observed_value=0.2,
            expected_value=0.8,
            deviation=0.6,
            severity=SeverityLevel.HIGH,
        )
        assert a.anomaly_id == "a1"
        assert a.layer == "c2"
        assert a.observed_value == 0.2
        assert a.expected_value == 0.8
        assert a.deviation == 0.6
        assert a.severity == SeverityLevel.HIGH

    def test_to_dict(self):
        a = Anomaly(
            anomaly_id="a2",
            layer="c0",
            metric="confidence",
            observed_value=0.3,
            expected_value=0.7,
            deviation=0.4,
            severity=SeverityLevel.MEDIUM,
            description="Test anomaly",
        )
        d = a.to_dict()
        assert d["severity"] == "medium"
        assert d["description"] == "Test anomaly"


class TestSeverityLevel:
    def test_all_levels(self):
        assert SeverityLevel.LOW.value == "low"
        assert SeverityLevel.MEDIUM.value == "medium"
        assert SeverityLevel.HIGH.value == "high"
        assert SeverityLevel.CRITICAL.value == "critical"


class TestSelfMonitor:
    def setup_method(self):
        self.monitor = SelfMonitor(history_size=10)

    def test_track_and_baseline(self):
        self.monitor.track("c1", "confidence", 0.8)
        self.monitor.track("c1", "confidence", 0.9)
        self.monitor.track("c1", "confidence", 0.7)
        baseline = self.monitor.get_baseline("c1", "confidence")
        assert baseline == pytest.approx(0.8, abs=0.05)

    def test_baseline_empty_returns_default(self):
        baseline = self.monitor.get_baseline("unknown", "unknown")
        assert baseline == 0.5

    def test_trend_stable(self):
        for v in [0.5, 0.5, 0.5, 0.5, 0.5]:
            self.monitor.track("c1", "confidence", v)
        trend = self.monitor.get_trend("c1", "confidence")
        assert trend == "stable"

    def test_trend_improving(self):
        for v in [0.5, 0.5, 0.5, 0.5, 0.9, 0.9]:
            self.monitor.track("c1", "confidence", v)
        trend = self.monitor.get_trend("c1", "confidence")
        assert trend == "improving"

    def test_trend_declining(self):
        for v in [0.9, 0.9, 0.9, 0.9, 0.5, 0.5]:
            self.monitor.track("c1", "confidence", v)
        trend = self.monitor.get_trend("c1", "confidence")
        assert trend == "declining"

    def test_trend_insufficient_data(self):
        self.monitor.track("c1", "confidence", 0.5)
        trend = self.monitor.get_trend("c1", "confidence")
        assert trend == "stable"

    def test_multiple_layers_and_metrics(self):
        self.monitor.track("c0", "confidence", 0.7)
        self.monitor.track("c1", "confidence", 0.8)
        self.monitor.track("c2", "confidence_estimate", 0.9)
        assert self.monitor.get_baseline("c0", "confidence") == 0.7
        assert self.monitor.get_baseline("c1", "confidence") == 0.8
        assert self.monitor.get_baseline("c2", "confidence_estimate") == 0.9

    def test_history_size_limit(self):
        for i in range(20):
            self.monitor.track("c1", "confidence", float(i) / 20)
        # History should be capped at 10
        values_list = list(self.monitor._history["c1"]["confidence"])
        assert len(values_list) <= 10

    def test_statistics(self):
        self.monitor.track("c1", "confidence", 0.8)
        self.monitor.track("c2", "confidence", 0.5)
        stats = self.monitor.get_statistics()
        assert stats["observations_tracked"] == 2
        assert stats["layers_tracked"] == 2

    def test_clear(self):
        self.monitor.track("c1", "confidence", 0.8)
        self.monitor.clear()
        assert self.monitor.get_baseline("c1", "confidence") == 0.5
        assert self.monitor.get_statistics()["observations_tracked"] == 0


class TestAnomalyDetector:
    def setup_method(self):
        self.detector = AnomalyDetector(
            low_threshold=0.1,
            medium_threshold=0.3,
            high_threshold=0.5,
        )

    def test_detect_no_anomaly_zero_deviation(self):
        obs = Observation("o1", "c1", "confidence", 0.8, baseline=0.8)
        baselines = {"c1": {"confidence": 0.8}}
        anomalies = self.detector.detect([obs], baselines)
        assert len(anomalies) == 0

    def test_detect_low_severity(self):
        obs = Observation("o1", "c1", "confidence", 0.75, baseline=0.8)
        baselines = {"c1": {"confidence": 0.8}}
        anomalies = self.detector.detect([obs], baselines)
        assert len(anomalies) == 1
        assert anomalies[0].severity == SeverityLevel.LOW

    def test_detect_medium_severity(self):
        obs = Observation("o1", "c1", "confidence", 0.6, baseline=0.8)
        baselines = {"c1": {"confidence": 0.8}}
        anomalies = self.detector.detect([obs], baselines)
        assert len(anomalies) == 1
        assert anomalies[0].severity == SeverityLevel.MEDIUM

    def test_detect_high_severity(self):
        obs = Observation("o1", "c1", "confidence", 0.35, baseline=0.8)
        baselines = {"c1": {"confidence": 0.8}}
        anomalies = self.detector.detect([obs], baselines)
        assert len(anomalies) == 1
        assert anomalies[0].severity == SeverityLevel.HIGH

    def test_detect_critical_severity(self):
        obs = Observation("o1", "c1", "confidence", 0.1, baseline=0.8)
        baselines = {"c1": {"confidence": 0.8}}
        anomalies = self.detector.detect([obs], baselines)
        assert len(anomalies) == 1
        assert anomalies[0].severity == SeverityLevel.CRITICAL

    def test_detect_multiple_anomalies(self):
        o1 = Observation("o1", "c1", "confidence", 0.2, baseline=0.8)
        o2 = Observation("o2", "c2", "confidence", 0.3, baseline=0.9)
        baselines = {"c1": {"confidence": 0.8}, "c2": {"confidence": 0.9}}
        anomalies = self.detector.detect([o1, o2], baselines)
        assert len(anomalies) == 2

    def test_anomaly_description_format(self):
        obs = Observation("o1", "c1", "confidence", 0.6, baseline=0.8)
        baselines = {"c1": {"confidence": 0.8}}
        anomalies = self.detector.detect([obs], baselines)
        assert len(anomalies) == 1
        assert "c1.confidence" in anomalies[0].description
        assert "deviated" in anomalies[0].description

    def test_clear_resets_statistics(self):
        obs = Observation("o1", "c1", "confidence", 0.2, baseline=0.8)
        baselines = {"c1": {"confidence": 0.8}}
        self.detector.detect([obs], baselines)
        self.detector.clear()
        assert self.detector.get_statistics()["anomalies_detected"] == 0

    def test_missing_baseline_defaults_to_0_5(self):
        obs = Observation("o1", "unknown_layer", "unknown_metric", 0.2)
        anomalies = self.detector.detect([obs], {})
        assert len(anomalies) >= 1


class TestObservationEngine:
    def setup_method(self):
        self.monitor = SelfMonitor(history_size=10)
        self.detector = AnomalyDetector()
        self.engine = ObservationEngine(
            monitor=self.monitor,
            detector=self.detector,
            memory=None,
        )

    def test_observe_layer_states(self):
        layer_states = {
            "c0": {"confidence": 0.7},
            "c1": {"confidence": 0.85},
        }
        observations = self.engine.observe(layer_states)
        assert len(observations) == 2
        assert {o.layer for o in observations} == {"c0", "c1"}

    def test_observe_ignores_non_dict_metrics(self):
        layer_states = {
            "c0": "not_a_dict",
            "c1": {"confidence": 0.85},
        }
        observations = self.engine.observe(layer_states)
        assert len(observations) == 1

    def test_observe_ignores_non_numeric_values(self):
        layer_states = {
            "c1": {"confidence": "not_a_number"},
        }
        observations = self.engine.observe({"c1": {"confidence": "not_a_number"}})
        assert len(observations) == 0

    def test_detect_anomalies_with_engine(self):
        # First populate some normal observations
        for _ in range(5):
            self.engine.observe({"c1": {"confidence": 0.8}})
        # Then observe an anomalous value
        observations = self.engine.observe({"c1": {"confidence": 0.1}})
        anomalies = self.engine.detect_anomalies(observations)
        assert len(anomalies) >= 1
        assert anomalies[0].layer == "c1"

    def test_detect_anomalies_empty_list(self):
        anomalies = self.engine.detect_anomalies([])
        assert len(anomalies) == 0

    def test_engine_statistics(self):
        self.engine.observe({"c1": {"confidence": 0.8}})
        stats = self.engine.get_statistics()
        assert stats["observations_made"] == 1
        assert "monitor" in stats
        assert "detector" in stats

    def test_engine_clear(self):
        self.engine.observe({"c1": {"confidence": 0.8}})
        self.engine.clear()
        stats = self.engine.get_statistics()
        assert stats["observations_made"] == 0
