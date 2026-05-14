"""Tests for claw-cog v1.5.0 modules."""
import time
import pytest
from claw_cog.time_consciousness import TimeConsciousnessModule, TimeConsciousnessResult
from claw_cog.predictive_processing import PredictiveProcessingModule, PredictiveResult


class TestTimeConsciousness:
    def setup_method(self):
        self.tc = TimeConsciousnessModule()

    def test_retain_and_get(self):
        self.tc.retain("event A", weight=0.8)
        self.tc.retain("event B", weight=0.6)
        retained = self.tc.get_retained(3)
        assert len(retained) == 2
        assert retained[0]["content"] == "event B"
        assert retained[0]["weight"] > 0

    def test_impress(self):
        self.tc.impress("current moment")
        imp = self.tc.get_impression()
        assert imp["content"] == "current moment"
        assert imp["intensity"] == 1.0

    def test_retention_depth(self):
        assert self.tc.get_retention_depth() == 0
        self.tc.retain("a")
        self.tc.retain("b")
        assert self.tc.get_retention_depth() == 2

    def test_protend_empty(self):
        result = self.tc.protend()
        assert result == []

    def test_protend_with_patterns(self):
        self.tc.learn_pattern("pattern_A")
        self.tc.retain("trigger event")
        protentions = self.tc.protend()
        assert len(protentions) > 0
        assert protentions[0]["pattern"] == "pattern_A"

    def test_full_cycle(self):
        self.tc.learn_pattern("daily_check")
        result = self.tc.process("hello world")
        assert len(result.retained_past) > 0
        assert result.current_impression["content"] == "hello world"
        assert 0.0 <= result.time_flow_score <= 1.0

    def test_decay_over_time(self):
        for i in range(10):
            self.tc.retain(f"event_{i}", weight=0.8 - i * 0.05)
        retained = self.tc.get_retained(10)
        # Older items should have lower weight
        assert retained[-1]["weight"] < retained[0]["weight"]


class TestPredictiveProcessing:
    def setup_method(self):
        self.pp = PredictiveProcessingModule()

    def test_update_and_predict(self):
        self.pp.update_model({"score": 0.7})
        self.pp.update_model({"score": 0.8})
        self.pp.update_model({"score": 0.75})
        pred = self.pp.predict("score")
        assert pred is not None
        assert 0.6 <= pred.expected_value <= 0.9

    def test_compute_error(self):
        self.pp.update_model({"score": 0.7})
        self.pp.update_model({"score": 0.8})
        err = self.pp.compute_error("score", 0.3)
        assert err is not None
        assert err.error > 0.2

    def test_predict_batch(self):
        self.pp.update_model({"a": 1.0, "b": 2.0})
        self.pp.update_model({"a": 1.2, "b": 2.1})
        preds = self.pp.predict_batch(["a", "b", "c"])
        assert len(preds) == 2

    def test_process_cycle(self):
        self.pp.update_model({"score": 0.6})
        self.pp.update_model({"score": 0.7})
        result = self.pp.process({"score": 0.65})
        assert result.accuracy > 0
        assert result.mse >= 0

    def test_accuracy_tracking(self):
        for i in range(5):
            self.pp.update_model({"x": float(i) / 10})
        self.pp.process({"x": 0.5})
        acc = self.pp.get_accuracy()
        assert 0.0 <= acc <= 1.0

    def test_convergence(self):
        """Model should converge with repeated similar inputs."""
        for _ in range(10):
            self.pp.process({"v": 0.75})
        pred = self.pp.predict("v")
        assert pred is not None
        assert abs(pred.expected_value - 0.75) < 0.2
