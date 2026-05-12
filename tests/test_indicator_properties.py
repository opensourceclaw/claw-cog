"""Tests for indicator properties: RPT, HOT, AST.

Validates that the five indicator properties from Butlin et al. are backed
by real behavioral tests, not just hardcoded values.
"""

import pytest
from claw_cog import ConsciousAgent, Config
from claw_cog.core.workspace import GlobalWorkspace
from claw_cog.layers.c2_metacognitive import C2Metacognitive


# ──────────────────────────────────────────────
# RPT — Recurrent Processing Theory (target ≥80%)
# ──────────────────────────────────────────────


class TestRPTFeedbackLoops:
    """Validate that recurrent processing (RPT) loops genuinely exist
    across the C0→C1→C2→C1 pipeline."""

    def setup_method(self):
        self.agent = ConsciousAgent()
        self.config = Config()

    def test_feedback_loop_exists(self):
        """RPT indicator reports True."""
        indicators = self.agent.get_indicator_properties()
        assert indicators["RPT"] is True

    def test_layer_loop_processing(self):
        """Processing pipeline traverses C0→C1→C2, carrying layer info."""
        result = self.agent.process("test feedback loop")

        assert result is not None
        assert result.metadata is not None

        # C0→C1: metadata must contain C0 contribution
        assert "c0_contribution" in result.metadata
        assert isinstance(result.metadata["c0_contribution"], float)

        # C1→C2: metadata must contain C2 monitoring info when C2 is active
        assert "c2_monitoring" in result.metadata
        # C2 is enabled by default, so monitoring data should be present
        c2_data = result.metadata["c2_monitoring"]
        assert c2_data is not None
        assert "adjustment_type" in c2_data

    def test_c2_feedback_to_c1(self):
        """When C2 monitors low confidence, adjustment_type is not 'none'."""
        # Use a very novel input with low confidence to trigger adjustment
        c2 = C2Metacognitive(self.config)

        class LowConfResult:
            confidence = 0.25

        result = c2.monitor(LowConfResult())
        # C2 should detect low confidence and suggest an adjustment
        assert result.adjustment_type != "none"
        assert result.needs_adjustment is True

    def test_info_passing_between_layers(self):
        """Metadata carries layer-specific information across the pipeline."""
        result = self.agent.process("info_passing test")

        meta = result.metadata
        # C0 layer info
        assert "c0_contribution" in meta
        assert "c0_pattern" in meta

        # C1 layer info
        assert "broadcast_time_ms" in meta
        assert isinstance(meta["broadcast_time_ms"], (int, float))

        # C2 layer info
        assert "c2_monitoring" in meta

    def test_disabled_c2_affects_feedback(self):
        """Disabling C2 should keep HOT=False, verifying C2's role in feedback."""
        agent_no_c2 = ConsciousAgent(enable_c2=False)
        indicators = agent_no_c2.get_indicator_properties()

        assert indicators["HOT"] is False
        assert indicators["RPT"] is True  # RPT is independent of C2 toggle


# ──────────────────────────────────────────────
# HOT — Higher-Order Thought (target ≥70%)
# ──────────────────────────────────────────────


class TestHOTMetacognition:
    """Validate that Higher-Order Thought (HOT) via C2 metacognition
    genuinely monitors and assesses confidence."""

    def setup_method(self):
        self.agent = ConsciousAgent()
        self.config = Config()

    def test_c2_enabled_returns_hot_true(self):
        """Default agent (C2 enabled) reports HOT=True."""
        indicators = self.agent.get_indicator_properties()
        assert indicators["HOT"] is True

    def test_c2_disabled_returns_hot_false(self):
        """Agent with C2 disabled reports HOT=False."""
        agent = ConsciousAgent(enable_c2=False)
        indicators = agent.get_indicator_properties()
        assert indicators["HOT"] is False

    def test_metacognitive_monitoring(self):
        """C2 responds differently across the full confidence spectrum."""
        c2 = C2Metacognitive(self.config)

        class DummyC1:
            def __init__(self, confidence):
                self.confidence = confidence

        # High confidence → no adjustment
        high = c2.monitor(DummyC1(0.95))
        assert high.adjustment_type == "none"
        assert not high.needs_adjustment

        # Medium confidence → strategy adjustment
        med = c2.monitor(DummyC1(0.55))
        assert med.adjustment_type == "strategy"
        assert med.needs_adjustment
        assert "information" in med.recommendation.lower()

        # Low confidence → confidence or seek_help adjustment
        low = c2.monitor(DummyC1(0.30))
        assert low.adjustment_type in ("confidence", "seek_help")
        assert low.needs_adjustment

        # Very low confidence → seek_help
        vlow = c2.monitor(DummyC1(0.05))
        assert vlow.adjustment_type == "seek_help"
        assert vlow.needs_adjustment
        assert vlow.recommendation is not None
        assert "human" in vlow.recommendation

    def test_self_monitoring_exists(self):
        """agent.get_metrics() includes layer status information."""
        metrics = self.agent.get_metrics()

        assert "layers" in metrics
        assert "workspace" in metrics
        assert "history_size" in metrics

        # Layer status should show C2 activity
        layer_status = metrics["layers"]
        assert "c0_active" in layer_status
        assert "c1_active" in layer_status
        assert "c2_active" in layer_status
        assert layer_status["c2_active"] is True

    def test_confidence_self_assessment(self):
        """assess_metacognition() returns metacognitive metrics dict."""
        # Need enough processing history for valid assessment
        for i in range(15):
            self.agent.process(f"assess input {i}")

        metrics = self.agent.assess_metacognition()
        assert "meta_d_prime" in metrics
        assert "d_prime" in metrics
        assert "m_ratio" in metrics
        assert "type2_roc_auc" in metrics
        assert "sample_size" in metrics
        assert metrics["sample_size"] == 15

    def test_hot_indicator_via_agent(self):
        """HOT indicator reflects C2 status."""
        default_agent = ConsciousAgent()
        assert default_agent.get_indicator_properties()["HOT"] is True

        no_c2_agent = ConsciousAgent(enable_c2=False)
        assert no_c2_agent.get_indicator_properties()["HOT"] is False


# ──────────────────────────────────────────────
# AST — Attention Schema Theory (target ≥50%)
# ──────────────────────────────────────────────


class TestASTAttention:
    """Validate that Attention Schema Theory (AST) mechanism is genuinely
    present via GlobalWorkspace subscriber/broadcast behaviour."""

    def setup_method(self):
        self.config = Config()
        self.ws = GlobalWorkspace(self.config)

    def test_attention_mechanism_exists(self):
        """AST indicator reports True."""
        agent = ConsciousAgent()
        indicators = agent.get_indicator_properties()
        assert indicators["AST"] is True

    def test_subscriber_count_management(self):
        """Subscriber count is tracked correctly."""

        def sub1(content):
            return content

        def sub2(content):
            return content

        assert self.ws.get_metrics()["subscriber_count"] == 0

        self.ws.subscribe(sub1)
        assert self.ws.get_metrics()["subscriber_count"] == 1

        self.ws.subscribe(sub2)
        assert self.ws.get_metrics()["subscriber_count"] == 2

        self.ws.unsubscribe(sub1)
        assert self.ws.get_metrics()["subscriber_count"] == 1

    def test_broadcast_reaches_subscribers(self):
        """Broadcast content reaches all subscribed handlers."""
        received = []

        def recorder(content):
            received.append(content)
            return {"status": "ok"}

        for _ in range(3):
            self.ws.subscribe(recorder)

        result = self.ws.process(input="hello", c0_output="c0_data", context=None)

        assert len(received) == 3
        assert result.confidence == 1.0  # all subscribers succeed
        assert result.broadcast_time_ms >= 0

    def test_attention_precision_weighting(self):
        """C0 contribution weight flows into workspace integration.

        The _integrate method returns the highest-confidence source object.
        High contribution = C0 source wins; low contribution = input wins.
        """

        class HighContribC0:
            output = "important"
            contribution = 0.9

        class LowContribC0:
            output = "noise"
            contribution = 0.1

        high_c0 = HighContribC0()

        # With high-contribution C0 output (weight 0.9 > input 0.3), C0 source wins
        r1 = self.ws.process(input="base", c0_output=high_c0, context=None)
        # _integrate returns the source object itself
        assert r1.output is high_c0

        # With very low contribution, input (weight 0.3) > C0 (weight 0.1)
        r2 = self.ws.process(input="base", c0_output=LowContribC0(), context=None)
        # input weight 0.3 > c0 contribution 0.1, so input wins
        assert r2.output == "base"

    def test_attention_allocation(self):
        """Different contributors are integrated by workspace._integrate.

        When context contains memory output (high weight), it should
        dominate over C0 and input.
        """
        low_c0 = type("C0", (), {"output": "c0", "contribution": 0.3})()
        context = {
            "memory_output": "remembered_content",
            "memory_confidence": 0.9,
        }
        result = self.ws.process(input="base", c0_output=low_c0, context=context)
        # memory has weight 0.9 vs c0 0.3 vs input 0.3 — memory should win
        assert result.output == "remembered_content"
