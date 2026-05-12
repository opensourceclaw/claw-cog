"""Tests for C0 Unconscious layer."""
import pytest
from claw_cog.config.defaults import Config
from claw_cog.layers.c0_unconscious import C0Unconscious, C0Result


class TestC0Unconscious:
    def setup_method(self):
        self.config = Config()
        self.c0 = C0Unconscious(self.config)

    def test_initialization(self):
        assert self.c0.is_active()
        assert not self.c0.get_pattern_count()

    def test_process_no_patterns_returns_impression(self):
        result = self.c0.process("some input")
        assert isinstance(result, C0Result)
        assert result.pattern_matched == "primal_impression"
        assert result.contribution == 0.3

    def test_pattern_registration(self):
        self.c0.add_pattern("greeting", ["hello", "world"])
        result = self.c0.process("hello world")
        assert result is not None  # pattern registered but may not match threshold
        assert result.contribution > 0.5

    def test_pattern_multi_keyword_scoring(self):
        self.c0.add_pattern("python", ["python", "code", "script", "function"])
        result = self.c0.process("write python code for a script")
        assert result.contribution > 0.6

    def test_auto_response_exact_match(self):
        self.config.c0_auto_response_enabled = True
        self.c0.add_auto_response("emergency", "STOP_EMERGENCY")
        result = self.c0.process("this is an emergency situation")
        assert result.pattern_matched == "auto_response"
        assert result.output == "STOP_EMERGENCY"

    def test_auto_response_regex_match(self):
        self.config.c0_auto_response_enabled = True
        self.c0.add_auto_response(r"regex:ERROR_\d{3}", "ERROR_HANDLER")
        result = self.c0.process("got ERROR_404 on the server")
        assert result.pattern_matched == "auto_response"

    def test_auto_response_disabled(self):
        self.config.c0_auto_response_enabled = False
        self.c0.add_auto_response("test", "response")
        result = self.c0.process("test this")
        assert result.pattern_matched != "auto_response"

    def test_impression_extracts_first_sentence(self):
        result = self.c0.process("First sentence. Second sentence. Third.")
        assert isinstance(result.output, str)
        assert "First" in result.output

    def test_metrics_tracking(self):
        self.c0.process("input 1")
        self.c0.process("input 2")
        metrics = self.c0.get_metrics()
        assert metrics["call_count"] == 2
        assert metrics["avg_time_ms"] > 0

    def test_non_string_input(self):
        result = self.c0.process(42)
        assert result.pattern_matched in ("default", "primal_impression")

    def test_no_auto_responses_when_none_registered(self):
        self.config.c0_auto_response_enabled = True
        result = self.c0.process("hello")
        assert result.pattern_matched != "auto_response"

    def test_reset_clears_metrics(self):
        self.c0.process("test")
        self.c0.reset()
        assert self.c0.get_metrics()["call_count"] == 0
