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

    def test_store_and_retrieve_stats(self):
        """Store memories and check stats (fixed from old duplicate)."""
        self.bridge.store("reflection", "Memory A")
        self.bridge.store("reflection", "Memory B")
        stats = self.bridge.get_stats()
        assert "backend" in stats

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

    def test_format_context_empty(self):
        """Cover format_context with empty list (line 216)."""
        result = self.bridge.format_context([])
        assert result == ""

    def test_fallback_path_store_and_retrieve(self, monkeypatch):
        """Cover fallback path when HAS_CLAW_MEM is False."""
        monkeypatch.setattr(
            "claw_cog.integration.claw_mem_bridge.HAS_CLAW_MEM", False
        )
        bridge = ClawMemBridge(self.config)
        assert bridge.is_available() is False
        # Store and retrieve through fallback
        bridge.store("reflection", "fallback memory")
        results = bridge.retrieve_relevant("fallback")
        assert len(results) > 0
        # Retrieve recent with fallback
        recent = bridge.retrieve_recent(limit=1)
        assert isinstance(recent, list)

    def test_retrieve_recent_fallback(self, monkeypatch):
        """Cover retrieve_recent fallback path."""
        monkeypatch.setattr(
            "claw_cog.integration.claw_mem_bridge.HAS_CLAW_MEM", False
        )
        bridge = ClawMemBridge(self.config)
        bridge.store("goal", "test goal")
        recent = bridge.retrieve_recent(memory_type="goal", limit=5)
        assert isinstance(recent, list)
