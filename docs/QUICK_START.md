# Quick Start

This guide walks you through installing claw-cog and using its core features.

---

## Installation

**Requirements**: Python ≥ 3.10

```bash
# Install from GitHub
pip install git+https://github.com/opensourceclaw/claw-cog.git

# Or with dev dependencies (testing, linting, benchmarking)
pip install "git+https://github.com/opensourceclaw/claw-cog.git[dev]"
```

Dependencies: `claw-mem` ≥ 2.8.0, `claw-rl` ≥ 2.7.0, `numpy`, `scipy`

---

## Your First Agent

```python
from claw_cog import ConsciousAgent

# Create an agent with default settings (C2 metacognition enabled)
agent = ConsciousAgent()

# Process input
result = agent.process("Hello, what can you help me with?")
print(result.output)       # → processed output
print(result.confidence)   # → e.g. 0.75
print(result.level.name)   # → e.g. C1_CONSCIOUS_ACCESS
```

---

## Understanding Indicator Properties

claw-cog tracks five consciousness indicators from the science of consciousness:

```python
indicators = agent.get_indicator_properties()
print(indicators)
# {'GWT': True, 'RPT': True, 'HOT': True, 'PP': False, 'AST': True}
```

| Key | Theory | Meaning |
|-----|--------|---------|
| GWT | Global Workspace | Information broadcast to all modules |
| RPT | Recurrent Processing | Feedback loops between layers |
| HOT | Higher-Order Thought | Self-monitoring metacognition |
| AST | Attention Schema | Attention mechanism for information |
| PP | Perceptual Presence | Sensory integration (v2.0.0) |

---

## Custom Configuration

```python
from claw_cog import Config, ConsciousAgent

config = Config(
    c0_pattern_threshold=0.6,      # Lower threshold = more pattern matches
    workspace_max_subscribers=20,  # More subscribers
    c2_high_threshold=0.9,         # Stricter trust threshold
)

agent = ConsciousAgent(config=config)
```

---

## Disabling Metacognition (C2)

For use cases where you want a lighter agent without self-monitoring:

```python
agent = ConsciousAgent(enable_c2=False)

# HOT indicator will be False
indicators = agent.get_indicator_properties()
assert indicators["HOT"] is False

# Processing still works, just without metacognitive monitoring
result = agent.process("Do something")
```

---

## Metacognitive Assessment

After processing enough inputs, evaluate the agent's metacognitive ability:

```python
# Process at least 10 inputs (default minimum)
for i in range(15):
    agent.process(f"Is this correct? Attempt {i}")

# Assess metacognition
metrics = agent.assess_metacognition()
print(f"d': {metrics['d_prime']:.4f}")          # Task performance
print(f"meta-d': {metrics['meta_d_prime']:.4f}") # Metacognitive ability
print(f"M-ratio: {metrics['m_ratio']:.4f}")      # Efficiency (~1.0 = optimal)
print(f"Type-2 AUC: {metrics['type2_roc_auc']:.4f}")

if "warning" in metrics:
    # Not enough data yet
    print(metrics["warning"])
```

---

## Working with Individual Layers

### C0: Pattern Matching

```python
from claw_cog.config.defaults import Config
from claw_cog.layers.c0_unconscious import C0Unconscious

c0 = C0Unconscious(Config())

# Register patterns
c0.add_pattern("greeting", ["hello", "hi", "hey", "greetings"])
c0.add_pattern("python", ["python", "code", "script", "debug"])

# Register auto-responses
c0.add_auto_response("help", "I can help you with various tasks.")

# Process
result = c0.process("I need help with python coding")
print(result.pattern_matched)  # → "python"
print(result.contribution)     # → e.g. 0.73
```

### C2: Metacognitive Monitoring

```python
from claw_cog.config.defaults import Config
from claw_cog.layers.c2_metacognitive import C2Metacognitive

c2 = C2Metacognitive(Config())

class MockResult:
    confidence = 0.35

result = c2.monitor(MockResult())
print(result.adjustment_type)  # → "confidence" or "seek_help"
print(result.needs_adjustment) # → True
```

### C2: Competence Assessment

```python
assessment = c2.assess_competence(
    "Implement a new user authentication system",
    known_situations=["Setup OAuth flow", "Configure JWT tokens", "Add login page"]
)
print(f"Competence: {assessment.score:.2f}")      # → e.g. 0.68
print(f"Risk level: {assessment.risk_level}")      # → "medium"
print(f"Recommendation: {assessment.recommendation}") # → "proceed_with_caution"
```

---

## Using the Global Workspace

```python
from claw_cog.config.defaults import Config
from claw_cog.core.workspace import GlobalWorkspace

ws = GlobalWorkspace(Config())

# Subscribe modules
def memory_module(content):
    return {"stored": content}

def logging_module(content):
    print(f"Broadcast: {content}")
    return {"logged": True}

ws.subscribe(memory_module)
ws.subscribe(logging_module)

# Process through workspace
result = ws.process(
    input="user message",
    c0_output="c0 processed output",
    context={"memory_output": "previous conversation context"}
)

print(f"Confidence: {result.confidence:.2f}")
print(f"Broadcast time: {result.broadcast_time_ms:.4f}ms")
print(f"Subscribers: {ws.get_metrics()['subscriber_count']}")
```

---

## Getting Metrics

```python
# Agent-wide metrics
metrics = agent.get_metrics()
print(metrics)
# {
#   "workspace": {"avg_broadcast_time_ms": ..., "total_broadcasts": ..., "subscriber_count": ...},
#   "layers": {"c0_active": True, "c1_active": True, "c2_active": True},
#   "history_size": 15
# }

# Layer-specific metrics
print(agent.layers.c0.get_metrics())
# {"call_count": 15, "avg_time_ms": X, "patterns_registered": 0, ...}

print(agent.layers.c2.get_monitor_stats())
# {"total_monitors": 15, "adjustments": {...}, "trusted_ratio": X}
```

---

## Running Tests

```bash
# All tests
pytest

# Excluding benchmarks
pytest tests/ -m "not benchmark"

# Benchmarks only
pytest tests/benchmarks/ -v

# With coverage
pytest --cov=claw_cog --cov-report=term-missing
```

---

## Next Steps

- [API Reference](API.md) — Full API documentation
- [Architecture](ARCHITECTURE.md) — System design and theory
- [Version Roadmap](VERSION_ROADMAP.md) — Release planning
- [Examples](../examples/) — More usage examples

---

## FAQ

**Q: Why is `assess_metacognition()` returning a warning?**

You need at least 10 processing rounds (default `assessment_min_samples`). Process more inputs first.

**Q: What happens if claw-mem is not installed?**

The `ClawMemBridge` falls back to basic in-memory keyword matching. Memory-dependent features will have reduced quality.

**Q: Can I run without C2?**

Yes — `ConsciousAgent(enable_c2=False)`. The HOT indicator will report `False`, and no metacognitive monitoring occurs.

**Q: Why is my confidence always around 0.5?**

Without registered C0 patterns or memory context, processing falls through to primal impression (contribution 0.3). Register patterns with `c0.add_pattern()` for higher contributions.

**Q: What errors can the agent raise?**

`ConfigurationError` — raised when `confidence_threshold` is not 0.0-1.0, or `Config.from_dict()` receives non-dict input. All exceptions inherit from `ClawCogError`.

**Q: What's the current test coverage?**

v1.0.0-alpha.3: 114 tests, 91% coverage.
