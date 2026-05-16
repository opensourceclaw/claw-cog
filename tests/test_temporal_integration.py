"""
Integration tests for temporal consciousness (ITCMA v1.5.0).

Tests the full C0→C1→C2 temporal pipeline integrated into ConsciousAgent.
"""

import pytest
from claw_cog import (
    ConsciousAgent, ConsciousnessLevel, ConsciousnessResultWithTime,
    Config, TemporalEvent, TemporalPattern, TemporalConflict,
)
from claw_cog.modules.temporal_perception import EventType
from claw_cog.modules.temporal_understanding import PatternType
from claw_cog.modules.temporal_prediction import ConflictType


@pytest.fixture
def agent():
    """Create a ConsciousAgent with temporal enabled."""
    config = Config(temporal_enabled=True)
    return ConsciousAgent(config=config)


@pytest.fixture
def agent_no_temporal():
    """Create a ConsciousAgent with temporal disabled."""
    config = Config(temporal_enabled=False)
    return ConsciousAgent(config=config)


class TestTemporalIntegration:
    """Integration tests for temporal consciousness pipeline."""

    def test_temporal_initialized_by_default(self):
        """Temporal modules should be initialized when config.temporal_enabled=True."""
        agent = ConsciousAgent()
        assert agent.config.temporal_enabled is True
        assert agent._temporal_perception is not None
        assert agent._temporal_understanding is not None
        assert agent._temporal_prediction is not None

    def test_process_returns_temporal_result(self, agent):
        """When temporal is enabled, process() should return ConsciousnessResultWithTime."""
        result = agent.process("meeting every day for 2 hours")
        assert isinstance(result, ConsciousnessResultWithTime)

    def test_process_returns_plain_result_when_temporal_off(self, agent_no_temporal):
        """When temporal is disabled, process() should return ProcessingResult."""
        from claw_cog import ProcessingResult
        result = agent_no_temporal.process("meeting every day")
        assert isinstance(result, ProcessingResult)
        assert not isinstance(result, ConsciousnessResultWithTime)

    def test_process_override_enable_temporal(self, agent_no_temporal):
        """enable_temporal parameter should override config."""
        result = agent_no_temporal.process(
            "meeting every day for 2 hours",
            enable_temporal=True,
        )
        assert isinstance(result, ConsciousnessResultWithTime)

    def test_process_override_disable_temporal(self, agent):
        """enable_temporal=False should disable even when config says True."""
        from claw_cog import ProcessingResult
        result = agent.process("meeting every day", enable_temporal=False)
        assert isinstance(result, ProcessingResult)
        assert not isinstance(result, ConsciousnessResultWithTime)


class TestTemporalEventDetection:
    """Test C0: Event detection in ConsciousAgent pipeline."""

    def test_detect_duration_event(self, agent):
        """Should detect duration event from input text."""
        result = agent.process("Code review meeting for 2 hours")
        assert isinstance(result, ConsciousnessResultWithTime)
        assert len(result.temporal_events) >= 1
        duration_events = [
            e for e in result.temporal_events
            if e.event_type == EventType.DURATION
        ]
        assert len(duration_events) >= 1
        assert duration_events[0].duration_seconds == 7200

    def test_detect_recurring_event(self, agent):
        """Should detect recurring event pattern."""
        result = agent.process("Standup meeting every day")
        assert len(result.temporal_events) >= 1
        recurring = [
            e for e in result.temporal_events
            if e.event_type == EventType.RECURRING
        ]
        assert len(recurring) >= 1
        assert recurring[0].recurrence_pattern == "daily"

    def test_detect_deadline_event(self, agent):
        """Should detect deadline expressions."""
        result = agent.process("Submit report by tomorrow")
        assert len(result.temporal_events) >= 1
        deadlines = [
            e for e in result.temporal_events
            if e.event_type == EventType.DEADLINE
        ]
        assert len(deadlines) >= 1

    def test_detect_instantaneous_event(self, agent):
        """Should detect instantaneous time expressions."""
        result = agent.process("Do this now")
        assert len(result.temporal_events) >= 1
        instant = [
            e for e in result.temporal_events
            if e.event_type == EventType.INSTANTANEOUS
        ]
        assert len(instant) >= 1

    def test_no_events_for_plain_text(self, agent):
        """Plain text without time expressions should have no events."""
        result = agent.process("Hello world")
        assert len(result.temporal_events) == 0


class TestTemporalPatternRecognition:
    """Test C1: Pattern recognition in ConsciousAgent pipeline."""

    def test_recognize_daily_pattern(self, agent):
        """Should recognize daily pattern from recurring events."""
        result = agent.process("每天开会 standup every day")
        patterns = result.temporal_patterns
        daily = [p for p in patterns if p.pattern_type == PatternType.DAILY]
        assert len(daily) >= 1

    def test_recognize_weekly_pattern(self, agent):
        """Should recognize weekly pattern."""
        result = agent.process("Sprint review every week")
        patterns = result.temporal_patterns
        weekly = [p for p in patterns if p.pattern_type == PatternType.WEEKLY]
        assert len(weekly) >= 1

    def test_pattern_has_metadata(self, agent):
        """Recognized patterns should have complete metadata."""
        result = agent.process("Code review every day for 3 hours")
        for pattern in result.temporal_patterns:
            assert pattern.description != ""
            assert pattern.confidence > 0
            assert pattern.event_count > 0

    def test_no_patterns_without_events(self, agent):
        """No patterns when there are no temporal events."""
        result = agent.process("Hello world")
        assert len(result.temporal_patterns) == 0


class TestTemporalPredictionAndConflicts:
    """Test C2: Prediction and conflict detection in ConsciousAgent pipeline."""

    def test_predict_discovers_conflicts(self, agent):
        """Should detect conflicts from patterns with multiple occurrences."""
        # A recurring pattern generates multiple predicted events within the horizon,
        # which can cause conflicts with each other
        result = agent.process("standup every day")
        assert isinstance(result, ConsciousnessResultWithTime)
        assert len(result.temporal_patterns) > 0

    def test_conflict_has_type_and_severity(self, agent):
        """Conflicts should include type and severity."""
        result = agent.process("meeting every day for 4 hours")
        for conflict in result.temporal_conflicts:
            assert conflict.conflict_type in list(ConflictType)
            assert conflict.severity in ("low", "medium", "high")

    def test_resolution_suggestions_for_conflicts(self, agent):
        """When conflicts exist, resolution suggestions should be generated."""
        result = agent.process("meeting every day for 4 hours")
        if result.temporal_conflicts:
            assert len(result.resolution_suggestions) == len(result.temporal_conflicts)
            for suggestion in result.resolution_suggestions:
                assert suggestion.strategy in ("reschedule", "allocate", "escalate")
                assert suggestion.feasibility > 0

    def test_deadline_alerts_for_high_severity(self, agent):
        """Deadline alerts should be generated for high-severity conflicts."""
        result = agent.process("meeting every day for 4 hours")
        if result.temporal_conflicts:
            high_conflicts = [c for c in result.temporal_conflicts if c.severity == "high"]
            assert len(result.deadline_alerts) <= len(high_conflicts)


class TestTemporalMetadata:
    """Test temporal metadata in ProcessingResult."""

    def test_metadata_includes_temporal_counts(self, agent):
        """Metadata should include temporal event/pattern/conflict counts."""
        result = agent.process("meeting every day for 2 hours by tomorrow")
        assert "temporal_events_count" in result.metadata
        assert "temporal_patterns_count" in result.metadata
        assert "temporal_conflicts_count" in result.metadata

    def test_custom_temporal_horizon(self, agent):
        """Config should control prediction horizon."""
        agent.config.temporal_horizon_days = 3
        result = agent.process("meeting every day for 2 hours")
        assert isinstance(result, ConsciousnessResultWithTime)


class TestTemporalMemoryIntegration:
    """Test time-aware memory features."""

    def test_memory_time_decay(self, agent):
        """Time decay should be higher for recent memories."""
        import time
        now = time.time()
        recent_weight = agent.memory.apply_time_decay(now)
        old_weight = agent.memory.apply_time_decay(now - 86400 * 30)
        assert recent_weight > old_weight
        assert 0.0 <= recent_weight <= 1.0
        assert 0.0 <= old_weight <= 1.0

    def test_memory_decay_none_timestamp(self, agent):
        """None timestamp should return low decay weight."""
        weight = agent.memory.apply_time_decay(None)
        assert weight == 0.1

    def test_memory_store_with_temporal(self, agent):
        """Should store memories with temporal metadata."""
        import time
        ts = time.time()
        success = agent.memory.store_with_temporal(
            "experience", "Test event",
            metadata={"priority": "high"},
            timestamp=ts,
        )
        assert success is True

    def test_memory_temporal_stats(self, agent):
        """Should return temporal statistics."""
        stats = agent.memory.get_temporal_stats()
        assert "total_memories" in stats
        assert "with_timestamps" in stats
        assert "backend" in stats


class TestTemporalConfig:
    """Test configuration options for temporal features."""

    def test_temporal_enabled_default(self):
        """temporal_enabled should default to True."""
        config = Config()
        assert config.temporal_enabled is True

    def test_temporal_disabled_config(self):
        """Disabling temporal should skip temporal processing."""
        config = Config(temporal_enabled=False)
        assert config.temporal_enabled is False

    def test_horizon_days_default(self):
        """temporal_horizon_days should default to 7."""
        config = Config()
        assert config.temporal_horizon_days == 7

    def test_decay_rate_default(self):
        """temporal_decay_rate should default to 0.1."""
        config = Config()
        assert config.temporal_decay_rate == 0.1

    def test_config_to_dict(self):
        """to_dict should include temporal fields."""
        config = Config(temporal_horizon_days=14, temporal_decay_rate=0.2)
        d = config.to_dict()
        assert d["temporal_horizon_days"] == 14
        assert d["temporal_decay_rate"] == 0.2

    def test_config_from_dict(self):
        """from_dict should parse temporal fields."""
        config = Config.from_dict({"temporal_horizon_days": 10})
        assert config.temporal_horizon_days == 10


class TestTemporalReset:
    """Test reset behavior with temporal modules."""

    def test_reset_clears_temporal_state(self, agent):
        """reset() should clear temporal module state."""
        agent.process("meeting every day for 2 hours")
        assert agent._temporal_perception.get_statistics()["events_detected"] > 0
        agent.reset()
        assert agent._temporal_perception.get_statistics()["events_detected"] == 0
        assert agent._temporal_prediction.get_statistics()["predictions_made"] == 0


class TestTemporalEndToEnd:
    """Full end-to-end pipeline tests."""

    def test_full_pipeline_with_temporal_input(self, agent):
        """Complete processing of temporal conversation."""
        inputs = [
            "Daily standup every day at 9am",
            "Sprint review every week for 2 hours",
            "Submit release by next Friday",
        ]

        for inp in inputs:
            result = agent.process(inp)
            assert isinstance(result, ConsciousnessResultWithTime)

        # Get comprehensive metrics
        metrics = agent.get_metrics()
        assert "temporal" in metrics
        assert "perception" in metrics["temporal"]
        assert "understanding" in metrics["temporal"]
        assert "prediction" in metrics["temporal"]

        # Check perception stats
        assert metrics["temporal"]["perception"]["events_detected"] > 0

    def test_pp_indicator_enabled_with_temporal(self, agent):
        """PP indicator should be True when temporal is enabled."""
        scores = agent.get_indicator_scores()
        assert scores["PP"] == 1.0

    def test_pp_indicator_disabled_without_temporal(self, agent_no_temporal):
        """PP indicator should be False when temporal is disabled."""
        scores = agent_no_temporal.get_indicator_scores()
        assert scores["PP"] == 0.0

    def test_rpt_temporal_integration_enabled(self, agent):
        """RPT temporal_integration should be True with temporal enabled."""
        props = agent.get_indicator_properties()
        assert props["RPT"]["temporal_integration"] is True

    def test_rpt_temporal_integration_disabled(self, agent_no_temporal):
        """RPT temporal_integration should be False with temporal disabled."""
        props = agent_no_temporal.get_indicator_properties()
        assert props["RPT"]["temporal_integration"] is False
