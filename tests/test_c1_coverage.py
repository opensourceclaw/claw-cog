"""Tests for C1 conscious layer (coverage boost)."""

import pytest
from unittest.mock import MagicMock
from claw_cog.config.defaults import Config
from claw_cog.layers.c1_conscious import C1Conscious, C1Result


class TestC1Conscious:
    @pytest.fixture
    def c1(self):
        config = Config()
        return C1Conscious(config)

    def test_process_without_memory(self, c1):
        result = c1.process("some content")
        assert isinstance(result, C1Result)
        assert result.output is not None

    def test_process_with_memory_bridge(self):
        config = Config()
        mock_mem = MagicMock()
        mock_mem.retrieve.return_value = {"memory": "ctx"}
        c1 = C1Conscious(config, memory_bridge=mock_mem)
        result = c1.process("test content")
        assert isinstance(result, C1Result)

    def test_process_dict_input(self, c1):
        result = c1.process({"key": "value"})
        assert isinstance(result, C1Result)

    def test_is_active(self, c1):
        assert c1.is_active() is True

    def test_reset(self, c1):
        c1.process("test")
        c1.reset()
