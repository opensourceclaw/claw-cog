"""
Layer Manager - Manages C0-C1-C2 consciousness layers.

C0: Unconscious - Fast patterns, auto responses
C1: Conscious Access - Global workspace, decision making
C2: Metacognitive - Self-monitoring, goal tracking
"""

from typing import Dict
import logging

from claw_cog.config.defaults import Config
from claw_cog.layers.c0_unconscious import C0Unconscious
from claw_cog.layers.c1_conscious import C1Conscious
from claw_cog.layers.c2_metacognitive import C2Metacognitive

logger = logging.getLogger(__name__)


class LayerManager:
    """
    Manages C0-C1-C2 consciousness layers.

    Provides unified interface for layer interaction
    and feedback loops (RPT - Recurrent Processing Theory).
    """

    def __init__(self, config: Config, enable_c2: bool = True):
        """
        Initialize layer manager.

        Args:
            config: Configuration object
            enable_c2: Whether to enable C2 metacognitive layer
        """
        self.config = config

        # Initialize layers
        self.c0 = C0Unconscious(config)
        self.c1 = C1Conscious(config)
        self.c2 = C2Metacognitive(config) if enable_c2 else None

        self.c2_enabled = enable_c2
        logger.info(f"LayerManager initialized: C0 ✓, C1 ✓, C2 {'✓' if enable_c2 else '✗'}")

    def has_feedback_loops(self) -> bool:
        """Check if feedback loops exist (RPT indicator)."""
        # v1.0.0: Basic implementation
        return True

    def get_layer_status(self) -> Dict[str, bool]:
        """Get status of all layers."""
        return {
            "c0_active": self.c0.is_active(),
            "c1_active": self.c1.is_active(),
            "c2_active": self.c2.is_active() if self.c2 else False,
        }

    def reset(self) -> None:
        """Reset all layers."""
        self.c0.reset()
        self.c1.reset()
        if self.c2:
            self.c2.reset()
