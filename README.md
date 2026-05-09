# claw-cog

<div align="center">

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-0.1.0-orange.svg)](https://github.com/opensourceclaw/claw-cog)

**Cognition Layer for AI Agents**

Self-Awareness • Reflection • Goal-Driven Intelligence

</div>

---

## Overview

**claw-cog** is the **Cognition Layer** of Project Neo, providing AI agents with self-awareness, reflective reasoning, and goal-driven capabilities. It builds on top of:

- **claw-mem**: Memory Layer (storage, retrieval, temporal reasoning)
- **claw-rl**: Learning Layer (feedback, rule extraction, optimization)

Together, these form the foundation for **Digital Consciousness**.

---

## Core Capabilities

### 1. Self-Awareness Module

```python
from claw_cog import SelfAwareness

awareness = SelfAwareness()
identity = awareness.get_identity()
# → "I am Friday, an AI assistant designed to help Peter..."

state = awareness.get_current_state()
# → "I am currently analyzing a project architecture..."
```

### 2. Reflective Reasoning Module

```python
from claw_cog import ReflectiveReasoning

reflection = ReflectiveReasoning()
result = reflection.reflect_on_action(action, outcome)
# → "This action succeeded because..."
```

### 3. Goal-Driven Module

```python
from claw_cog import GoalDriven

goal_system = GoalDriven()
goal_system.set_goal("Complete neoclaw v3.1 development")
progress = goal_system.evaluate_progress()
# → "25% complete, 3 sub-goals remaining"
```

---

## Architecture

```
┌─────────────────────────────────────────┐
│           Cognition Layer (claw-cog)     │
│  Self-Awareness | Reflection | Goals    │
├─────────────────────────────────────────┤
│           Learning Layer (claw-rl)       │
│  Feedback | Rules | Optimization         │
├─────────────────────────────────────────┤
│           Memory Layer (claw-mem)        │
│  Store | Retrieve | Temporal | Context  │
└─────────────────────────────────────────┘
```

---

## Installation

```bash
# From GitHub (recommended during development)
pip install git+https://github.com/opensourceclaw/claw-cog.git

# With development dependencies
pip install "git+https://github.com/opensourceclaw/claw-cog.git[dev]"
```

---

## Quick Start

```python
from claw_cog import CognitionEngine

# Initialize cognition engine
engine = CognitionEngine(
    memory_provider="claw-mem",
    learning_provider="claw-rl"
)

# Self-awareness
identity = engine.who_am_i()
print(identity)
# → Identity(name="Friday", role="AI Assistant", ...)

# Reflection
reflection = engine.reflect("Why did the last task fail?")
print(reflection.insight)

# Goal pursuit
engine.set_goal("Help user complete the project")
progress = engine.evaluate_progress()
```

---

## Project Structure

```
claw-cog/
├── src/
│   └── claw_cog/
│       ├── __init__.py
│       ├── self_awareness.py      # Self-awareness module
│       ├── reflective.py          # Reflective reasoning
│       ├── goal_driven.py         # Goal-driven behavior
│       ├── boundary.py            # Capability & ethical boundaries
│       ├── engine.py              # Cognition engine
│       └── bridge.py              # Integration with claw-mem/rl
├── tests/
│   ├── test_self_awareness.py
│   ├── test_reflective.py
│   └── test_goal_driven.py
├── docs/
│   ├── architecture.md
│   └── api-reference.md
├── skill/
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
├── benchmarks/
├── examples/
├── pyproject.toml
└── README.md
```

---

## Development Status

| Version | Status | Focus |
|---------|--------|-------|
| **v0.1.0** | 🚧 Alpha | Core architecture, basic self-awareness |
| **v0.2.0** | Planned | Reflective reasoning, goal decomposition |
| **v0.3.0** | Planned | Integration with claw-mem/rl |
| **v1.0.0** | Future | Production-ready cognition layer |

---

## Integration with Project Neo

claw-cog is part of **Project Neo**:

| Project | Role | Status |
|---------|------|--------|
| **claw-mem** | Memory Layer | ✅ Production |
| **claw-rl** | Learning Layer | ✅ Production |
| **claw-cog** | Cognition Layer | 🚧 Alpha |
| **neoclaw** | Integration Layer | ✅ Active |

---

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

---

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

---

## Links

- **GitHub**: https://github.com/opensourceclaw/claw-cog
- **Documentation**: https://github.com/opensourceclaw/claw-cog/tree/main/docs
- **Project Neo**: https://github.com/opensourceclaw

---

<div align="center">

*Building Digital Consciousness, One Layer at a Time*

</div>
