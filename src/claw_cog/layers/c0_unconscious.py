"""
C0: Unconscious Layer.

Fast pattern matching, automatic responses, primal impressions.
Based on Freud's Id and Husserl's Primal Impression.
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging
import re

from claw_cog.config.defaults import Config

logger = logging.getLogger(__name__)


@dataclass
class C0Result:
    """Result from C0 unconscious processing."""

    output: Any
    contribution: float
    pattern_matched: str
    processing_time_ms: float = 0.0


class C0Unconscious:
    """C0: Unconscious Layer — fast pattern matching, auto responses,
    primal impression formation. Operates below awareness threshold."""

    def __init__(self, config: Config):
        self.config = config
        self._patterns: Dict[str, List[str]] = {}
        self._auto_responses: Dict[str, Any] = {}
        self._active = True
        self._call_count: int = 0
        self._total_time_ms: float = 0.0
        logger.debug("C0Unconscious layer initialized")

    def process(self, input: Any, context: Optional[Dict] = None) -> C0Result:
        """Process input through unconscious mechanisms.

        1. Check auto-response triggers
        2. Match against known patterns
        3. Form primal impression as fallback
        """
        from time import time
        self._call_count += 1
        start = time()

        # 1. Auto-response: check exact and regex triggers
        auto_response = self._check_auto_response(input)
        if auto_response is not None:
            elapsed = (time() - start) * 1000
            self._total_time_ms += elapsed
            return C0Result(
                output=auto_response,
                contribution=0.8,
                pattern_matched="auto_response",
                processing_time_ms=elapsed,
            )

        # 2. Pattern matching: weighted multi-pattern matching
        pattern_name, match_score = self._match_pattern(input)
        if match_score > self.config.c0_pattern_threshold:
            elapsed = (time() - start) * 1000
            self._total_time_ms += elapsed
            return C0Result(
                output=input,
                contribution=match_score,
                pattern_matched=pattern_name,
                processing_time_ms=elapsed,
            )

        # 3. Primal impression: extract key features
        impression = self._form_impression(input)
        elapsed = (time() - start) * 1000
        self._total_time_ms += elapsed
        return C0Result(
            output=impression,
            contribution=0.3,
            pattern_matched="primal_impression",
            processing_time_ms=elapsed,
        )

    def _match_pattern(self, input: Any) -> Tuple[str, float]:
        """Match input against known patterns using multi-keyword scoring."""
        if not isinstance(input, str):
            return ("default", 0.5)

        if not self._patterns:
            return ("default", 0.5)

        best_name = "default"
        best_score = 0.0
        input_lower = input.lower()

        for pattern_name, keywords in self._patterns.items():
            matched = sum(1 for kw in keywords if kw.lower() in input_lower)
            total = len(keywords) if keywords else 1
            score = min(1.0, matched / total * 0.8 + 0.2)

            if score > best_score:
                best_score = score
                best_name = pattern_name

        return (best_name, best_score)

    def _check_auto_response(self, input: Any) -> Optional[Any]:
        """Check if input triggers an automatic response.

        Supports exact match, prefix match, and regex patterns.
        """
        if not self.config.c0_auto_response_enabled:
            return None
        if not self._auto_responses:
            return None

        if isinstance(input, str):
            input_lower = input.lower()
            for trigger, response in self._auto_responses.items():
                if trigger.startswith("regex:"):
                    pattern = trigger[6:]
                    try:
                        if re.search(pattern, input):
                            return response
                    except re.error:
                        pass
                elif trigger.lower() in input_lower:
                    return response

        return None

    def _form_impression(self, input: Any) -> Any:
        """Form primal impression from input — extract key features."""
        if isinstance(input, str):
            # Extract first meaningful segment
            sentences = [s.strip() for s in input.split(".") if s.strip()]
            if sentences:
                return sentences[0][:200]
        return input

    def add_pattern(self, name: str, keywords: List[str]) -> None:
        """Add a named pattern with trigger keywords."""
        self._patterns[name] = keywords

    def add_auto_response(self, trigger: str, response: Any) -> None:
        """Add an automatic response triggered by keyword or regex.

        Args:
            trigger: Keyword to match, or 'regex:<pattern>' for regex.
            response: Response to return on match.
        """
        self._auto_responses[trigger] = response

    def get_pattern_count(self) -> int:
        """Number of registered patterns."""
        return len(self._patterns)

    def get_metrics(self) -> Dict[str, Any]:
        """Get C0 performance metrics."""
        return {
            "call_count": self._call_count,
            "avg_time_ms": (
                self._total_time_ms / self._call_count
                if self._call_count > 0 else 0.0
            ),
            "patterns_registered": len(self._patterns),
            "auto_responses_registered": len(self._auto_responses),
        }

    def is_active(self) -> bool:
        return self._active

    def reset(self) -> None:
        self._call_count = 0
        self._total_time_ms = 0.0
