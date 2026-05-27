"""
ClawMem Bridge - Integration with claw-mem memory system.

Provides memory storage and retrieval for consciousness modules.
v1.5.0: Added time-aware memory features (time decay, time-range search).
"""

from typing import Any, Dict, List, Optional
import logging
import math
import time
from datetime import datetime

from claw_cog.config.defaults import Config

logger = logging.getLogger(__name__)

# Try to import claw-mem
try:
    from claw_mem import MemoryManager

    HAS_CLAW_MEM = True
except ImportError:
    HAS_CLAW_MEM = False
    logger.warning("claw-mem not available, using in-memory fallback")


MEMORY_TYPE_MAP = {
    "reflection": "episodic",
    "experience": "episodic",
    "goal": "semantic",
    "pattern": "procedural",
}


class ClawMemBridge:
    """
    Bridge between claw-cog and claw-mem.

    Provides:
    - Memory storage for reflections and experiences
    - Context retrieval for consciousness processing
    - Temporal memory access (recent, related)

    Example:
        >>> bridge = ClawMemBridge()
        >>> bridge.store("reflection", "I should be more careful")
        >>> context = bridge.retrieve_relevant("careful")
    """

    def __init__(self, config: Config):
        """
        Initialize claw-mem bridge.

        Args:
            config: Configuration object
        """
        self.config = config

        if HAS_CLAW_MEM:
            self._memory = MemoryManager()
            logger.info("ClawMemBridge initialized with claw-mem backend")
        else:
            # In-memory fallback
            self._memory_fallback: Dict[str, List[Dict]] = {
                "reflections": [],
                "experiences": [],
                "goals": [],
                "patterns": [],
            }
            logger.info("ClawMemBridge initialized with in-memory fallback")

    def store(
        self,
        memory_type: str,
        content: Any,
        metadata: Optional[Dict] = None,
    ) -> bool:
        """
        Store memory entry.

        Args:
            memory_type: Type of memory (reflection, experience, goal, pattern)
            content: Memory content
            metadata: Optional metadata

        Returns:
            bool: Success status
        """
        # Map claw-cog types to claw-mem supported types
        mapped_type = MEMORY_TYPE_MAP.get(memory_type, memory_type)

        valid_types = {"episodic", "semantic", "procedural", "critical_rule"}
        if mapped_type not in valid_types:
            logger.warning(f"Unknown memory type: {memory_type}, falling back to episodic")
            mapped_type = "episodic"

        try:
            if HAS_CLAW_MEM:
                self._memory.store(
                    content=str(content),
                    memory_type=mapped_type,
                    metadata={
                        "original_type": memory_type,
                        **(metadata or {}),
                    },
                )
            else:
                # Fallback storage
                if mapped_type not in self._memory_fallback:
                    self._memory_fallback[mapped_type] = []

                self._memory_fallback[mapped_type].append(
                    {
                        "content": content,
                        "metadata": {
                            "original_type": memory_type,
                            **(metadata or {}),
                        },
                    }
                )

            logger.debug(f"Stored {memory_type} (as {mapped_type}): {str(content)[:50]}...")
            return True

        except Exception as e:
            logger.error(f"Failed to store memory: {e}")
            return False

    def retrieve_relevant(
        self,
        query: str,
        memory_types: Optional[List[str]] = None,
        limit: int = 10,
    ) -> List[Dict]:
        """
        Retrieve relevant memories.

        Args:
            query: Search query
            memory_types: Types of memories to search
            limit: Maximum results

        Returns:
            List of relevant memories
        """
        try:
            if HAS_CLAW_MEM:
                results = self._memory.search(
                    query=query,
                    limit=limit,
                )
                return [
                    {
                        "content": r.get("text", ""),
                        "type": r.get("memory_type", "unknown"),
                        "score": r.get("score", 0.0),
                    }
                    for r in results
                ]
            else:
                # Fallback: simple keyword matching
                results = []
                types = memory_types or list(self._memory_fallback.keys())

                for mem_type in types:
                    if mem_type not in self._memory_fallback:
                        continue

                    for entry in self._memory_fallback[mem_type]:
                        content = str(entry.get("content", ""))
                        if query.lower() in content.lower():
                            results.append(
                                {
                                    "content": content,
                                    "type": mem_type,
                                    "score": 0.5,  # Default score
                                }
                            )

                return results[:limit]

        except Exception as e:
            logger.error(f"Failed to retrieve memories: {e}")
            return []

    def retrieve_recent(
        self,
        memory_type: Optional[str] = None,
        limit: int = 5,
    ) -> List[Dict]:
        """
        Retrieve recent memories.

        Args:
            memory_type: Type of memories to retrieve
            limit: Maximum results

        Returns:
            List of recent memories
        """
        try:
            if HAS_CLAW_MEM:
                # Use search with recent filter
                results = self._memory.search(
                    query="",
                    limit=limit,
                )
                return [
                    {"content": r.get("text", ""), "type": r.get("memory_type", "")}
                    for r in results
                ]
            else:
                # Fallback: get most recent
                if memory_type and memory_type in self._memory_fallback:
                    entries = self._memory_fallback[memory_type][-limit:]
                else:
                    # Get from all types
                    all_entries = []
                    for entries in self._memory_fallback.values():
                        all_entries.extend(entries)
                    entries = all_entries[-limit:]

                return [
                    {"content": e.get("content", ""), "type": e.get("metadata", {}).get("type", "")}
                    for e in entries
                ]

        except Exception as e:
            logger.error(f"Failed to retrieve recent memories: {e}")
            return []

    def format_context(
        self,
        memories: List[Dict],
        max_tokens: int = 1000,
    ) -> str:
        """
        Format memories as context string.

        Args:
            memories: List of memories
            max_tokens: Approximate max tokens

        Returns:
            Formatted context string
        """
        if not memories:
            return ""

        lines = []
        current_length = 0
        max_chars = max_tokens * 4  # Rough approximation

        for mem in memories:
            content = mem.get("content", "")
            mem_type = mem.get("type", "unknown")

            line = f"[{mem_type}] {content}"
            if current_length + len(line) > max_chars:
                break

            lines.append(line)
            current_length += len(line)

        return "\n".join(lines)

    # ── v1.5.0: Time-aware memory features ────────────────────────────────────

    def apply_time_decay(
        self,
        timestamp: Optional[float],
        decay_rate: Optional[float] = None,
        reference_time: Optional[float] = None,
    ) -> float:
        """
        Calculate time-decayed relevance weight for a memory.

        Uses exponential decay: weight = exp(-decay_rate * age_days)
        Fresher memories get higher weight.

        Args:
            timestamp: Unix timestamp of the memory (None = assume old)
            decay_rate: Decay rate per day (default from config)
            reference_time: Reference time (default: now)

        Returns:
            float: Decay weight between 0.0 and 1.0
        """
        if timestamp is None:
            return 0.1

        if decay_rate is None:
            decay_rate = self.config.temporal_decay_rate

        ref = reference_time or time.time()
        age_seconds = max(0, ref - timestamp)
        age_days = age_seconds / 86400.0

        return math.exp(-decay_rate * age_days)

    def search_by_time_range(
        self,
        start_time: datetime,
        end_time: datetime,
        memory_types: Optional[List[str]] = None,
        limit: int = 50,
    ) -> List[Dict]:
        """
        Search memories within a specific time range.

        Args:
            start_time: Start of the time range
            end_time: End of the time range
            memory_types: Types of memories to search (None = all)
            limit: Maximum results

        Returns:
            List of memory dicts within the time range
        """
        try:
            if HAS_CLAW_MEM:
                results = self._memory.search(
                    query="",
                    limit=limit,
                )
                filtered = [
                    {
                        "content": r.get("text", ""),
                        "type": r.get("memory_type", ""),
                        "metadata": r.get("metadata", {}),
                    }
                    for r in results
                    if start_time <= datetime.fromtimestamp(r.get("timestamp", 0)) <= end_time
                ]
                return filtered[:limit]
            else:
                # Fallback: approximate by checking metadata timestamps
                results = []
                types = memory_types or list(self._memory_fallback.keys())
                for mem_type in types:
                    if mem_type not in self._memory_fallback:
                        continue
                    for entry in self._memory_fallback[mem_type]:
                        ts = entry.get("metadata", {}).get("timestamp", 0)
                        if ts:
                            try:
                                entry_time = datetime.fromtimestamp(ts)
                                if start_time <= entry_time <= end_time:
                                    results.append(
                                        {
                                            "content": entry.get("content", ""),
                                            "type": mem_type,
                                            "metadata": entry.get("metadata", {}),
                                        }
                                    )
                            except (OSError, ValueError):
                                continue
                return results[:limit]

        except Exception as e:
            logger.error(f"Failed to search by time range: {e}")
            return []

    def store_with_temporal(
        self,
        memory_type: str,
        content: Any,
        metadata: Optional[Dict] = None,
        timestamp: Optional[float] = None,
    ) -> bool:
        """
        Store memory with temporal metadata (v1.5.0).

        Attaches timestamp and temporal type info for time-aware retrieval.

        Args:
            memory_type: Type of memory
            content: Memory content
            metadata: Optional metadata
            timestamp: Unix timestamp (default: now)

        Returns:
            bool: Success status
        """
        ts = timestamp or time.time()
        enhanced_metadata = {
            **(metadata or {}),
            "timestamp": ts,
            "iso_datetime": datetime.fromtimestamp(ts).isoformat(),
        }
        return self.store(memory_type, content, enhanced_metadata)

    def get_temporal_stats(self) -> Dict:
        """Get temporal statistics for stored memories."""
        stats: Dict[str, Any] = {
            "total_memories": 0, "with_timestamps": 0,
            "oldest_ts": None, "newest_ts": None,
        }

        if HAS_CLAW_MEM:
            stats["backend"] = "claw-mem"
            stats["total_memories"] = "unknown (external backend)"
        else:
            stats["backend"] = "fallback"
            for entries in self._memory_fallback.values():
                for entry in entries:
                    stats["total_memories"] += 1  # type: ignore[operator]
                    ts = entry.get("metadata", {}).get("timestamp")
                    if ts:
                        stats["with_timestamps"] += 1
                        if stats["oldest_ts"] is None or ts < stats["oldest_ts"]:  # type: ignore[operator]
                            stats["oldest_ts"] = ts
                        if stats["newest_ts"] is None or ts > stats["newest_ts"]:
                            stats["newest_ts"] = ts

        return stats

    def is_available(self) -> bool:
        """Check if claw-mem is available."""
        return HAS_CLAW_MEM

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        if HAS_CLAW_MEM:
            # Get from claw-mem
            return {"backend": "claw-mem"}
        else:
            return {
                "backend": "fallback",
                **{k: len(v) for k, v in self._memory_fallback.items()},
            }
