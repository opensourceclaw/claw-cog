"""Configuration defaults for claw-cog."""

from dataclasses import dataclass
from typing import Any, Dict

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

    # Temporal consciousness settings (v1.5.0 ITCMA)
    temporal_enabled: bool = True
    temporal_horizon_days: int = 7
    temporal_retention_capacity: int = 1000
    temporal_decay_rate: float = 0.1
    temporal_confidence_threshold: float = 0.5

    # Volition settings (v1.8.0 V/O layer)
    volition_enabled: bool = True
    volition_max_goals: int = 10
    volition_intention_buffer_size: int = 5

    # Observation settings (v1.8.0 V/O layer)
    observation_enabled: bool = True
    observation_history_size: int = 100
    observation_anomaly_low_threshold: float = 0.1
    observation_anomaly_medium_threshold: float = 0.3
    observation_anomaly_high_threshold: float = 0.5

    # Verification settings (v4.0.0)
    verification_enabled: bool = True
    verification_quality_completeness_threshold: float = 0.5
    verification_quality_clarity_threshold: float = 0.5
    verification_quality_safety_threshold: float = 0.8
    verification_quality_relevance_threshold: float = 0.5
    verification_calibration_ece_threshold: float = 0.1
    verification_calibration_num_bins: int = 10
    verification_consistency_deviation_threshold: float = 0.3

    # Governance settings (v4.0.0 Phase 3)
    governance_enabled: bool = True
    governance_level: str = "medium"  # low / medium / high
    governance_audit_max_records: int = 1000

    # Performance settings
    enable_profiling: bool = False
    log_level: str = "INFO"

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "Config":
        """Create config from dictionary."""
        if not isinstance(config_dict, dict):
            raise ConfigurationError(f"Expected a dict, got {type(config_dict).__name__}")
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
            "temporal_enabled": self.temporal_enabled,
            "temporal_horizon_days": self.temporal_horizon_days,
            "temporal_retention_capacity": self.temporal_retention_capacity,
            "temporal_decay_rate": self.temporal_decay_rate,
            "temporal_confidence_threshold": self.temporal_confidence_threshold,
            "volition_enabled": self.volition_enabled,
            "volition_max_goals": self.volition_max_goals,
            "volition_intention_buffer_size": self.volition_intention_buffer_size,
            "observation_enabled": self.observation_enabled,
            "observation_history_size": self.observation_history_size,
            "observation_anomaly_low_threshold": self.observation_anomaly_low_threshold,
            "observation_anomaly_medium_threshold": self.observation_anomaly_medium_threshold,
            "observation_anomaly_high_threshold": self.observation_anomaly_high_threshold,
            "verification_enabled": self.verification_enabled,
            "verification_quality_completeness_threshold": self.verification_quality_completeness_threshold,
            "verification_quality_clarity_threshold": self.verification_quality_clarity_threshold,
            "verification_quality_safety_threshold": self.verification_quality_safety_threshold,
            "verification_quality_relevance_threshold": self.verification_quality_relevance_threshold,
            "verification_calibration_ece_threshold": self.verification_calibration_ece_threshold,
            "verification_calibration_num_bins": self.verification_calibration_num_bins,
            "verification_consistency_deviation_threshold": self.verification_consistency_deviation_threshold,
            "governance_enabled": self.governance_enabled,
            "governance_level": self.governance_level,
            "governance_audit_max_records": self.governance_audit_max_records,
            "enable_profiling": self.enable_profiling,
            "log_level": self.log_level,
        }
