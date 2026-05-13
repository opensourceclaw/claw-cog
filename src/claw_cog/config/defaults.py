"""Configuration defaults for claw-cog."""

from dataclasses import dataclass, field
from typing import Dict

from claw_cog.exceptions import ConfigurationError


@dataclass
class Config:
    """claw-cog configuration."""

    # Global Workspace settings
    workspace_broadcast_timeout_ms: int = 100
    workspace_max_subscribers: int = 10

    # C0 Unconscious settings
    c0_pattern_threshold: float = 0.7
    c0_auto_response_enabled: bool = True

    # C1 Conscious Access settings
    c1_integration_method: str = "weighted_average"
    c1_confidence_threshold: float = 0.7

    # C2 Metacognitive settings
    c2_enabled: bool = True
    c2_high_threshold: float = 0.8
    c2_medium_threshold: float = 0.5
    c2_low_threshold: float = 0.3

    # Metacognitive assessment settings
    assessment_min_samples: int = 5
    assessment_history_size: int = 1000

    # Memory settings
    memory_backend: str = "claw-mem"
    memory_context_max_tokens: int = 4000

    # Performance settings
    enable_profiling: bool = False
    log_level: str = "INFO"

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "Config":
        """Create config from dictionary."""
        if not isinstance(config_dict, dict):
            raise ConfigurationError(
                f"Expected a dict, got {type(config_dict).__name__}"
            )
        return cls(**{k: v for k, v in config_dict.items() if hasattr(cls, k)})

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "workspace_broadcast_timeout_ms": self.workspace_broadcast_timeout_ms,
            "workspace_max_subscribers": self.workspace_max_subscribers,
            "c0_pattern_threshold": self.c0_pattern_threshold,
            "c0_auto_response_enabled": self.c0_auto_response_enabled,
            "c1_integration_method": self.c1_integration_method,
            "c1_confidence_threshold": self.c1_confidence_threshold,
            "c2_enabled": self.c2_enabled,
            "c2_high_threshold": self.c2_high_threshold,
            "c2_medium_threshold": self.c2_medium_threshold,
            "c2_low_threshold": self.c2_low_threshold,
            "assessment_min_samples": self.assessment_min_samples,
            "assessment_history_size": self.assessment_history_size,
            "memory_backend": self.memory_backend,
            "memory_context_max_tokens": self.memory_context_max_tokens,
            "enable_profiling": self.enable_profiling,
            "log_level": self.log_level,
        }
