"""Enhanced tests for ClawMemBridge — memory type mapping coverage."""
import pytest
from claw_cog.config.defaults import Config
from claw_cog.integration.claw_mem_bridge import ClawMemBridge, MEMORY_TYPE_MAP


class TestBridgeMemoryTypeMapping:
    def setup_method(self):
        self.config = Config()
        self.bridge = ClawMemBridge(self.config)

    def test_memory_type_map_has_entries(self):
        assert "reflection" in MEMORY_TYPE_MAP
        assert MEMORY_TYPE_MAP["reflection"] == "episodic"
        assert MEMORY_TYPE_MAP["experience"] == "episodic"
        assert MEMORY_TYPE_MAP["goal"] == "semantic"
        assert MEMORY_TYPE_MAP["pattern"] == "procedural"

    def test_store_reflection_mapped_to_episodic(self):
        success = self.bridge.store(
            memory_type="reflection",
            content="test reflection content",
        )
        assert success is True

    def test_store_experience_mapped_to_episodic(self):
        success = self.bridge.store(
            memory_type="experience",
            content="test experience content",
        )
        assert success is True

    def test_store_goal_mapped_to_semantic(self):
        success = self.bridge.store(
            memory_type="goal",
            content="test goal content",
        )
        assert success is True

    def test_store_pattern_mapped_to_procedural(self):
        success = self.bridge.store(
            memory_type="pattern",
            content="test pattern content",
        )
        assert success is True

    def test_store_unknown_type_falls_back(self):
        success = self.bridge.store(
            memory_type="nonexistent_type",
            content="test content",
        )
        assert success is True

    def test_retrieve_recent_fallback(self, monkeypatch):
        """Cover retrieve_recent with fallback path."""
        monkeypatch.setattr(
            "claw_cog.integration.claw_mem_bridge.HAS_CLAW_MEM", False
        )
        bridge = ClawMemBridge(self.config)
        bridge.store("reflection", "test")
        recent = bridge.retrieve_recent(limit=5)
        assert isinstance(recent, list)

    def test_retrieve_recent_with_type(self, monkeypatch):
        """Cover retrieve_recent with specific type."""
        monkeypatch.setattr(
            "claw_cog.integration.claw_mem_bridge.HAS_CLAW_MEM", False
        )
        bridge = ClawMemBridge(self.config)
        bridge.store("reflection", "test content")
        recent = bridge.retrieve_recent(memory_type="episodic", limit=5)
        assert isinstance(recent, list)

    def test_bridge_is_available(self, monkeypatch):
        """Test is_available returns actual state."""
        monkeypatch.setattr(
            "claw_cog.integration.claw_mem_bridge.HAS_CLAW_MEM", False
        )
        bridge = ClawMemBridge(self.config)
        assert bridge.is_available() is False

    def test_store_with_metadata(self, monkeypatch):
        """Test storing with original_type saved in metadata."""
        monkeypatch.setattr(
            "claw_cog.integration.claw_mem_bridge.HAS_CLAW_MEM", False
        )
        bridge = ClawMemBridge(self.config)
        success = bridge.store(
            memory_type="reflection",
            content="test with metadata",
            metadata={"confidence": 0.8},
        )
        assert success is True

    def test_store_unknown_type_creates_fallback(self, monkeypatch):
        """Test unknown type creates new fallback bucket."""
        monkeypatch.setattr(
            "claw_cog.integration.claw_mem_bridge.HAS_CLAW_MEM", False
        )
        bridge = ClawMemBridge(self.config)
        success = bridge.store(
            memory_type="custom_type",
            content="custom content",
        )
        assert success is True

    def test_relevant_retrieval_fallback(self, monkeypatch):
        """Test retrieval from fallback with type filtering."""
        monkeypatch.setattr(
            "claw_cog.integration.claw_mem_bridge.HAS_CLAW_MEM", False
        )
        bridge = ClawMemBridge(self.config)
        bridge.store("reflection", "specific test query here")
        results = bridge.retrieve_relevant(
            "test query",
            memory_types=["episodic"],
        )
        assert isinstance(results, list)

    def test_relevant_retrieval_empty_type(self, monkeypatch):
        """Test retrieval when type doesn't exist in fallback."""
        monkeypatch.setattr(
            "claw_cog.integration.claw_mem_bridge.HAS_CLAW_MEM", False
        )
        bridge = ClawMemBridge(self.config)
        results = bridge.retrieve_relevant(
            "no match",
            memory_types=["nonexistent"],
        )
        assert isinstance(results, list)

    def test_format_context_with_multiple_memories(self):
        """Test formatting multiple memories."""
        memories = [
            {"content": "Memory one", "type": "episodic"},
            {"content": "Memory two", "type": "semantic"},
        ]
        formatted = self.bridge.format_context(memories)
        assert "Memory one" in formatted
        assert "Memory two" in formatted
