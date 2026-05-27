"""Tests for observation engine (coverage boost)."""

import pytest
from claw_cog.modules.observation.engine import ObservationEngine
from claw_cog.modules.observation.self_monitor import SelfMonitor
from claw_cog.modules.observation.anomaly_detector import AnomalyDetector


class TestObservationEngine:
    @pytest.fixture
    def engine(self):
        monitor = SelfMonitor()
        detector = AnomalyDetector()
        return ObservationEngine(monitor, detector, memory=None)

    def test_observe_basic(self, engine):
        layer_states = {
            "c0": {"processing_time_ms": 5.0, "contribution": 0.8},
            "c1": {"confidence": 0.9},
        }
        obs = engine.observe(layer_states)
        assert isinstance(obs, list)

    def test_detect_anomalies_empty(self, engine):
        anomalies = engine.detect_anomalies([])
        assert anomalies == []

    def test_detect_anomalies(self, engine):
        layer_states = {
            "c0": {"processing_time_ms": 5.0, "contribution": 0.8},
            "c1": {"confidence": 0.9},
        }
        obs = engine.observe(layer_states)
        anomalies = engine.detect_anomalies(obs)
        assert isinstance(anomalies, list)

    def test_get_statistics(self, engine):
        stats = engine.get_statistics()
        assert isinstance(stats, dict)

    def test_clear(self, engine):
        engine.observe({"c0": {"processing_time_ms": 5.0}})
        engine.clear()
