# claw-cog

Cognition Layer for AI Agents

## Installation

```bash
npx clawhub@latest install opensourceclaw-claw-cog
```

## Description

claw-cog provides self-awareness, reflective reasoning, and goal-driven capabilities for AI agents. It is the Cognition Layer of Project Neo, working alongside:

- claw-mem (Memory Layer)
- claw-rl (Learning Layer)

## Core Modules

### 1. Self-Awareness
- Know who I am (identity)
- Know what I'm doing (current state)
- Know why I'm doing it (intention)

### 2. Reflective Reasoning
- Metacognitive analysis
- Causal reasoning
- Lesson extraction

### 3. Goal-Driven
- Goal decomposition
- Progress tracking
- Autonomous pursuit

## Usage

```python
from claw_cog import CognitionEngine

engine = CognitionEngine()

# Self-awareness
identity = engine.who_am_i()

# Reflection
insight = engine.reflect("Why did this happen?")

# Goal pursuit
engine.set_goal("Complete the task")
progress = engine.evaluate_progress()
```

## Requirements

- Python 3.8+
- claw-mem >= 2.8.0
- claw-rl >= 2.7.0

## Links

- GitHub: https://github.com/opensourceclaw/claw-cog
- Project Neo: https://github.com/opensourceclaw
