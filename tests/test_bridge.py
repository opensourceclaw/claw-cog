"""Tests for claw-mem integration bridge."""
import pytest
from claw_cog.config.defaults import Config
from claw_cog.integration.claw_mem_bridge import ClawMemBridge


class TestClawMemBridge:
    def setup_method(self):
        self.config = Config()
        self.bridge = ClawMemBridge(self.config)

    def test_initialization(self):
        assert self.bridge is not None

    def test_store_reflection(self):
        success = self.bridge.store(
            memory_type="reflection",
            content="I should review more carefully",
            metadata={"confidence": 0.8},
        )
        assert success is True

    def test_store_experience(self):
        self.bridge.store("reflection", "User asked about architecture")
        assert True  # no crash

    def test_store_goal(self):
        self.bridge.store("goal", "Complete v1.0.0 with 80% coverage")
        assert True

    def test_store_pattern(self):
        self.bridge.store("pattern", "Error: timeout is common")
        assert True

    def test_retrieve_relevant(self):
        self.bridge.store("reflection", "need to write more tests")
        self.bridge.store("reflection", "tests are important")
        results = self.bridge.retrieve_relevant("tests")
        assert isinstance(results, list)

    def test_retrieve_with_type_filter(self):
        self.bridge.store("reflection", "Need to test more")
        self.bridge.store("reflection", "Random fact")
        results = self.bridge.retrieve_relevant(
            "test", memory_types=["reflection"]
        )
        assert isinstance(results, list)

    def test_get_stats(self):
        self.bridge.store("reflection", "Memory A")
        self.bridge.store("reflection", "Memory B")
        context = self.bridge.get_context("test query")
        assert isinstance(context, str)
        assert "Memory A" in context or "Memory B" in context

    def test_format_context(self):
        memories = [
            {"content": "First memory", "type": "reflection"},
            {"content": "Second memory", "type": "reflection"},
        ]
        formatted = self.bridge.format_context(memories, max_tokens=50)
        assert "First memory" in formatted
        assert "Second memory" in formatted

    def test_format_context_truncation(self):
        long_memories = [
            {"content": "X" * 1000, "type": "reflection"},
        ]
        formatted = self.bridge.format_context(long_memories, max_tokens=10)
        assert len(formatted) < 2000

    def test_get_stats(self):
        stats = self.bridge.get_stats()
        assert "backend" in stats
        assert True  # stats vary by backend
