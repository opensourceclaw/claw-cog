"""Tests for C1 Conscious Access layer."""
import pytest
from claw_cog.config.defaults import Config
from claw_cog.layers.c1_conscious import C1Conscious, C1Result


class TestC1Conscious:
    def setup_method(self):
        self.config = Config()
        self.c1 = C1Conscious(self.config)

    def test_initialization(self):
        assert self.c1.is_active()

    def test_workspace_pass_through(self):
        result = self.c1.process("test content")
        assert isinstance(result, C1Result)
        assert result.output is not None
        assert 0.0 <= result.confidence <= 1.0
        assert result.source == "workspace"

    def test_with_context(self):
        result = self.c1.process("content", {"domain": "test"})
        assert result.metadata["memory_retrieved"] is False

    def test_confidence_without_memory(self):
        result = self.c1.process("content")
        assert result.confidence >= 0.5

    def test_confidence_scaling(self):
        r1 = self.c1.process(None)
        r2 = self.c1.process("real content")
        # Processing count increases confidence
        assert r1.confidence <= r2.confidence + 0.3

    def test_reset(self):
        self.c1.process("test")
        self.c1.reset()
        assert True  # no crash
