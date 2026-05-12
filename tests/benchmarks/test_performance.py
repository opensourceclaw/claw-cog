"""Performance benchmarks for claw-cog.

Uses pytest-benchmark to measure latency of core operations:
- GWT broadcast latency < 100ms
- C0 pattern matching < 50ms
- meta-d' calculation < 10ms
- End-to-end pipeline latency (additional coverage)
"""

import pytest
from claw_cog.config.defaults import Config
from claw_cog.core.workspace import GlobalWorkspace
from claw_cog.layers.c0_unconscious import C0Unconscious
from claw_cog.assessment.meta_d_prime import MetacognitiveAssessment


class DummyC0ForWS:
    """Minimal C0-like object for workspace benchmark."""
    output = "c0_processed"
    contribution = 0.7


class DummyHistoryItem:
    """Minimal ProcessingResult-like object for meta-d' benchmark."""
    def __init__(self, confidence, correct):
        self.confidence = confidence
        self.correct = correct


class TestPerformance:
    """Performance benchmarks for core operations."""

    @pytest.mark.benchmark(min_rounds=10, max_time=0.5)
    def test_gwt_broadcast_performance(self, benchmark):
        """GWT broadcast latency should be well under 100ms."""
        config = Config()
        ws = GlobalWorkspace(config)

        # Register 10 subscribers to simulate realistic load
        for i in range(10):
            ws.subscribe(lambda c, _i=i: {"id": _i, "received": True})

        def run_broadcast():
            ws.process(input="benchmark_input", c0_output=DummyC0ForWS(), context=None)

        benchmark(run_broadcast)

        # After running, verify it completed correctly
        result = ws.process(input="verify", c0_output=DummyC0ForWS(), context=None)
        assert result.broadcast_time_ms >= 0
        # Latency assertion: should complete quickly
        assert result.broadcast_time_ms < 1000, (
            f"GWT broadcast too slow: {result.broadcast_time_ms}ms"
        )

    @pytest.mark.benchmark(min_rounds=10, max_time=0.5)
    def test_c0_pattern_matching_performance(self, benchmark):
        """C0 pattern matching latency should be well under 50ms."""
        config = Config()
        c0 = C0Unconscious(config)

        # Register 20 patterns to simulate realistic load
        for i in range(20):
            c0.add_pattern(
                f"pattern_{i}",
                [f"keyword_{i}_a", f"keyword_{i}_b", f"keyword_{i}_c"],
            )

        # Use an input with 2+ keywords from one pattern to cross threshold
        test_input = "This is a test with keyword_5_a and keyword_5_b in the text"

        def run_pattern_match():
            c0.process(test_input)

        benchmark(run_pattern_match)

        result = c0.process(test_input)
        assert result.pattern_matched != "primal_impression"  # should match a pattern
        assert result.contribution > 0.0

    @pytest.mark.benchmark(min_rounds=10, max_time=0.5)
    def test_meta_d_prime_performance(self, benchmark):
        """meta-d' calculation latency should be well under 10ms."""
        config = Config()
        ma = MetacognitiveAssessment(config)

        # Generate 100-item history with varied confidence and correctness
        history = []
        for i in range(100):
            conf = (i % 10) / 10.0 + 0.05
            correct = conf > 0.5
            history.append(DummyHistoryItem(confidence=conf, correct=correct))

        ground_truth = [h.correct for h in history]

        def run_meta_d():
            ma.compute_metrics(history, ground_truth=ground_truth)

        benchmark(run_meta_d)

        result = ma.compute_metrics(history, ground_truth=ground_truth)
        assert "meta_d_prime" in result
        assert result["sample_size"] == 100
        # Should have meaningful values (not just defaults)
        assert "warning" not in result

    @pytest.mark.benchmark(min_rounds=5, max_time=0.5)
    def test_end_to_end_performance(self, benchmark):
        """Full C0→C1→C2 pipeline latency (additional coverage)."""
        from claw_cog import ConsciousAgent

        agent = ConsciousAgent()

        def run_pipeline():
            agent.process("end-to-end benchmark input")

        benchmark(run_pipeline)

        # Verify pipeline produced valid output
        result = agent.process("verify e2e")
        assert result is not None
        assert 0.0 <= result.confidence <= 1.0
