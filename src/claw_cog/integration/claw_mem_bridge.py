"""
ClawMem Bridge - Integration with claw-mem memory system.

Provides memory storage and retrieval for consciousness modules.
"""

from typing import Any, Dict, List, Optional
import logging

from claw_cog.config.defaults import Config

logger = logging.getLogger(__name__)

# Try to import claw-mem
try:
    from claw_mem import MemoryManager
    HAS_CLAW_MEM = True
except ImportError:
    HAS_CLAW_MEM = False
    logger.warning("claw-mem not available, using in-memory fallback")


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
        try:
            if HAS_CLAW_MEM:
                self._memory.store(
                    content=str(content),
                    memory_type=memory_type,
                    metadata=metadata or {},
                )
            else:
                # Fallback storage
                if memory_type not in self._memory_fallback:
                    self._memory_fallback[memory_type] = []

                self._memory_fallback[memory_type].append({
                    "content": content,
                    "metadata": metadata or {},
                })

            logger.debug(f"Stored {memory_type}: {str(content)[:50]}...")
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
                            results.append({
                                "content": content,
                                "type": mem_type,
                                "score": 0.5,  # Default score
                            })

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

    def is_available(self) -> bool:
        """Check if claw-mem is available."""
        return HAS_CLAW_MEM

    def get_stats(self) -> Dict[str, int]:
        """Get memory statistics."""
        if HAS_CLAW_MEM:
            # Get from claw-mem
            return {"backend": "claw-mem"}
        else:
            return {
                "backend": "fallback",
                **{k: len(v) for k, v in self._memory_fallback.items()},
            }
