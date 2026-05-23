# claw-cog

<div align="center">

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-1.5.0-blue.svg)](https://github.com/opensourceclaw/claw-cog)

**AI Consciousness Component for AI Agent**

Global Workspace · C0-C1-C2 Architecture · Metacognitive Assessment

</div>

---

## Overview

**claw-cog** is the **Consciousness Layer** of OpenClaw, implementing AI consciousness capabilities based on established cognitive neuroscience theories:

- **Global Workspace Theory** (GNWT) — Baars, Dehaene
- **C0-C1-C2 Layered Architecture** — Dehaene et al.
- **meta-d' Metacognition** — Maniscalco & Lau

It builds on [claw-mem](https://github.com/opensourceclaw/claw-mem) (memory) and [claw-rl](https://github.com/opensourceclaw/claw-rl) (learning), together forming **Digital Consciousness**.

---

## Architecture

```
┌──────────────────────────────────────────────┐
│              C2: Metacognitive                │
│     Self-Monitoring · Confidence Assessment   │
│          Goal Tracking · Protention           │
├──────────────────────────────────────────────┤
│          C1: Conscious Access (GWT)           │
│    Global Workspace · Integration · Broadcast │
├──────────────────────────────────────────────┤
│             C0: Unconscious                   │
│     Pattern Matching · Auto Responses ·       │
│            Primal Impressions                 │
└──────────────────────────────────────────────┘
         ↕                        ↕
    claw-mem (Memory)      claw-rl (Learning)
```

**Processing Pipeline**: `Input → Memory Retrieval → C0 Pattern Match → C1 Workspace Broadcast → C2 Metacognitive Monitor → Output`

**Indicator Properties** (Butlin et al.):

| Theory | Indicator | v1.0.0 |
|--------|-----------|:------:|
| GWT | Global Workspace Theory | ✅ |
| RPT | Recurrent Processing Theory | ✅ |
| HOT | Higher-Order Thought Theory | ✅ |
| AST | Attention Schema Theory | ✅ |
| PP | Perceptual Presence | v2.0.0 |

---

## Installation

```bash
pip install git+https://github.com/opensourceclaw/claw-cog.git

# With dev dependencies (testing, linting, benchmarking)
pip install "git+https://github.com/opensourceclaw/claw-cog.git[dev]"
```

**Requirements**: Python ≥ 3.10, [claw-mem](https://github.com/opensourceclaw/claw-mem) ≥ 2.8.0

---

## Quick Start

```python
from claw_cog import ConsciousAgent

# Create an agent (C2 metacognition enabled by default)
agent = ConsciousAgent()

# Process input through consciousness layers
result = agent.process("What is the current project status?")
print(f"Output: {result.output}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Level: {result.level.name}")

# Check consciousness indicator properties
indicators = agent.get_indicator_properties()
# → {"GWT": True, "RPT": True, "HOT": True, "PP": False, "AST": True}

# Assess metacognitive ability (needs 10+ processing rounds)
metrics = agent.assess_metacognition()
print(f"meta-d': {metrics['meta_d_prime']}")
print(f"M-ratio: {metrics['m_ratio']}")
```

**Custom Configuration**:

```python
from claw_cog import Config, ConsciousAgent

config = Config(
    c2_enabled=True,
    c0_pattern_threshold=0.6,
    workspace_max_subscribers=20,
)
agent = ConsciousAgent(config=config)
```

**Without C2** (lighter, no metacognition):

```python
agent = ConsciousAgent(enable_c2=False)
# HOT indicator will be False
```

---

## Core Components

| Component | Description |
|-----------|-------------|
| `ConsciousAgent` | Main entry point — orchestrates the full pipeline |
| `GlobalWorkspace` | GNWT implementation — subscriber broadcast + integration |
| `LayerManager` | Manages C0/C1/C2 layers and feedback loops |
| `C0Unconscious` | Fast pattern matching, auto responses, primal impressions |
| `C1Conscious` | Memory retrieval, integration, decision making |
| `C2Metacognitive` | Self-monitoring, confidence assessment, competence awareness |
| `MetacognitiveAssessment` | meta-d' framework for metacognitive evaluation |
| `ClawMemBridge` | Memory integration bridge to claw-mem |
| `ConfigurationError` | Configuration validation error |
| `ClawCogError` | Base exception for all claw-cog errors |

---

## Development

```bash
# Run tests
pytest                                 # All tests
pytest tests/ -m "not benchmark"       # Skip benchmarks

# Benchmark
pytest tests/benchmarks/ -v            # Performance tests

# Coverage
pytest --cov=claw_cog --cov-report=html
```

**Current Status**: RC (v1.0.0-rc.2) — 200+ tests, 89% coverage, API frozen

---

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

---

<div align="center">

*Building Digital Consciousness, One Layer at a Time*

</div>
