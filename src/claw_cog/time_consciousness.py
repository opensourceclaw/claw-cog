"""Time Consciousness Module (ITCMA) — Retention/Impression/Protention for claw-cog v1.5.0.

Based on Husserl's phenomenology: retention (past holding), impression (present),
protention (future anticipation). Implements the ITCMA (Internal Time Consciousness
Model Architecture) framework.
"""

import logging
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class TimeSlice:
    """A single moment in the time consciousness stream."""
    timestamp: float = field(default_factory=time.time)
    content: Any = None
    retention_weight: float = 0.5  # how strongly it's retained
    impression_intensity: float = 1.0  # initial impression strength
    protention_horizon: float = 0.0  # predicted future relevance


@dataclass
class TimeConsciousnessResult:
    """Result of time consciousness processing."""
    retained_past: List[Dict[str, Any]] = field(default_factory=list)
    current_impression: Dict[str, Any] = field(default_factory=dict)
    protended_future: List[Dict[str, Any]] = field(default_factory=list)
    time_flow_score: float = 0.5


class TimeConsciousnessModule:
    """ITCMA: Internal Time Consciousness Model Architecture.

    Three components:
    - Retention: holds past experiences with exponential decay
    - Impression: captures the present moment with full intensity
    - Protention: anticipates future events based on patterns
    """

    def __init__(self, retention_capacity: int = 20, decay_rate: float = 0.1):
        self.retention_capacity = retention_capacity
        self.decay_rate = decay_rate
        self._retention_buffer: deque = deque(maxlen=retention_capacity)
        self._current_impression: Optional[TimeSlice] = None
        self._protention_horizon: float = 3.0  # seconds into future
        self._event_patterns: Dict[str, List[float]] = {}

    # ── Retention (Past) ──────────────────────────

    def retain(self, content: Any, weight: float = 0.5) -> None:
        """Hold a past experience in retention buffer."""
        self._retention_buffer.append(TimeSlice(
            content=content,
            retention_weight=weight,
            impression_intensity=weight,
        ))

    def get_retained(self, lookback: int = 5) -> List[Dict[str, Any]]:
        """Get recent retained experiences with decay applied."""
        retained = []
        for i, ts in enumerate(reversed(list(self._retention_buffer)[-lookback:])):
            decayed = ts.retention_weight * (1.0 - self.decay_rate * i)
            retained.append({
                "content": ts.content,
                "weight": round(max(0.0, decayed), 4),
                "timestamp": ts.timestamp,
                "age": i,
            })
        return retained

    def get_retention_depth(self) -> int:
        return len(self._retention_buffer)

    # ── Impression (Present) ──────────────────────

    def impress(self, content: Any) -> None:
        """Capture the present moment as current impression."""
        self._current_impression = TimeSlice(
            content=content,
            impression_intensity=1.0,
        )
        self.retain(content, weight=1.0)

    def get_impression(self) -> Dict[str, Any]:
        if not self._current_impression:
            return {}
        return {
            "content": self._current_impression.content,
            "intensity": self._current_impression.impression_intensity,
            "timestamp": self._current_impression.timestamp,
            "retention_count": len(self._retention_buffer),
        }

    # ── Protention (Future) ────────────────────────

    def protend(self, context: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Anticipate likely future events based on retained patterns."""
        protentions = []
        if not self._retention_buffer:
            return protentions

        # Pattern-based protention
        recent = list(self._retention_buffer)[-5:]
        for pattern_name, timestamps in self._event_patterns.items():
            if timestamps:
                avg_interval = (
                    sum(timestamps[-3:]) / len(timestamps[-3:])
                    if len(timestamps) >= 3 else timestamps[-1]
                )
                relevance = 1.0 / max(0.1, avg_interval)
                protentions.append({
                    "pattern": pattern_name,
                    "estimated_in": round(avg_interval / 1000, 2),
                    "confidence": round(min(1.0, relevance), 4),
                })

        # Sort by confidence
        protentions.sort(key=lambda x: x["confidence"], reverse=True)
        return protentions[:5]

    def learn_pattern(self, pattern_name: str) -> None:
        """Record an event pattern for protention learning."""
        if pattern_name not in self._event_patterns:
            self._event_patterns[pattern_name] = []
        self._event_patterns[pattern_name].append(time.time())

    # ── Full Cycle ─────────────────────────────────

    def process(self, content: Any, context: Optional[Dict] = None) -> TimeConsciousnessResult:
        """Run a full retention-impression-protention cycle."""
        self.impress(content)
        retained = self.get_retained(5)
        protended = self.protend(context)

        flow_score = self._compute_flow()
        logger.debug("Time cycle: retention=%d protention=%d flow=%.2f",
                     len(retained), len(protended), flow_score)

        return TimeConsciousnessResult(
            retained_past=retained,
            current_impression=self.get_impression(),
            protended_future=protended,
            time_flow_score=round(flow_score, 4),
        )

    def _compute_flow(self) -> float:
        """Compute time flow score: higher = smoother temporal continuity."""
        if len(self._retention_buffer) < 2:
            return 0.5
        recent = list(self._retention_buffer)[-5:]
        intervals = []
        for i in range(1, len(recent)):
            intervals.append(recent[i].timestamp - recent[i-1].timestamp)
        if not intervals:
            return 0.5
        avg = sum(intervals) / len(intervals)
        return max(0.0, min(1.0, 1.0 - (avg / 10.0)))
