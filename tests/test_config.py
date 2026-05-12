"""Tests for Config serialization and validation."""
import pytest
from claw_cog.config.defaults import Config
from claw_cog.exceptions import ConfigurationError


class TestConfigSerialization:
    def setup_method(self):
        self.config = Config()

    def test_to_dict_roundtrip(self):
        d = self.config.to_dict()
        assert isinstance(d, dict)
        restored = Config.from_dict(d)
        assert restored.workspace_broadcast_timeout_ms == \
            self.config.workspace_broadcast_timeout_ms

    def test_from_dict_partial_keys(self):
        c = Config.from_dict({"c2_enabled": False})
        assert c.c2_enabled is False
        assert c.c1_confidence_threshold == 0.7  # default

    def test_from_dict_raises_on_non_dict(self):
        with pytest.raises(ConfigurationError):
            Config.from_dict("not_a_dict")
        with pytest.raises(ConfigurationError):
            Config.from_dict(123)

    def test_to_dict_all_keys(self):
        d = self.config.to_dict()
        expected_keys = [
            "workspace_broadcast_timeout_ms",
            "workspace_max_subscribers",
            "c0_pattern_threshold",
            "c0_auto_response_enabled",
            "c1_integration_method",
            "c1_confidence_threshold",
            "c2_enabled",
            "c2_high_threshold",
            "c2_medium_threshold",
            "c2_low_threshold",
            "assessment_min_samples",
            "assessment_history_size",
            "memory_backend",
            "memory_context_max_tokens",
            "enable_profiling",
            "log_level",
        ]
        for key in expected_keys:
            assert key in d

    def test_from_dict_ignores_unknown_keys(self):
        c = Config.from_dict({"unknown_key": "value", "c2_enabled": False})
        assert c.c2_enabled is False
        assert not hasattr(c, "unknown_key")
