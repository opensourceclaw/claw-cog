"""Tests for C0 unconscious layer (coverage boost)."""

import pytest
from claw_cog.config.defaults import Config
from claw_cog.layers.c0_unconscious import C0Unconscious, C0Result


class TestC0Unconscious:
    @pytest.fixture
    def c0(self):
        config = Config()
        return C0Unconscious(config)

    def test_process_basic(self, c0):
        result = c0.process("hello world")
        assert isinstance(result, C0Result)
        assert 0.0 <= result.contribution <= 1.0

    def test_process_with_context(self, c0):
        result = c0.process("test input", {"key": "val"})
        assert isinstance(result, C0Result)

    def test_add_and_match_pattern(self, c0):
        c0.add_pattern("greeting", ["hello", "hi"])
        result = c0.process("hello world")
        assert result.contribution > 0.0

    def test_add_pattern_increases_count(self, c0):
        c0.add_pattern("test1", ["a", "b"])
        c0.add_pattern("test2", ["c", "d"])
        assert c0.get_pattern_count() == 2

    def test_auto_response(self, c0):
        c0.add_auto_response("ping", "pong")
        result = c0.process("ping")
        assert result.output == "pong"

    def test_auto_response_disabled(self):
        config = Config(c0_auto_response_enabled=False)
        c0 = C0Unconscious(config)
        c0.add_auto_response("ping", "pong")
        result = c0.process("ping")
        assert isinstance(result, C0Result)

    def test_get_metrics(self, c0):
        c0.process("hello")
        metrics = c0.get_metrics()
        assert "patterns_registered" in metrics

    def test_is_active(self, c0):
        assert c0.is_active() is True

    def test_reset(self, c0):
        c0.add_pattern("test", ["x"])
        c0.reset()
        assert isinstance(c0.get_metrics(), dict)

    def test_empty_input(self, c0):
        result = c0.process("")
        assert isinstance(result, C0Result)

    def test_list_input(self, c0):
        result = c0.process(["item1", "item2"])
        assert isinstance(result, C0Result)
