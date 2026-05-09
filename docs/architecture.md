# Architecture Overview

## System Architecture

claw-cog implements the **Cognition Layer** of Project Neo, providing AI agents with self-awareness, reflective reasoning, and goal-driven capabilities.

## Layer Stack

```
┌─────────────────────────────────────────┐
│           Application Layer             │
│     (neoclaw, user applications)        │
├─────────────────────────────────────────┤
│        Cognition Layer (claw-cog)       │
│  Self-Awareness | Reflection | Goals    │
├─────────────────────────────────────────┤
│        Learning Layer (claw-rl)         │
│  Feedback | Rules | Optimization        │
├─────────────────────────────────────────┤
│         Memory Layer (claw-mem)         │
│  Store | Retrieve | Temporal | Context  │
└─────────────────────────────────────────┘
```

## Core Modules

### 1. Self-Awareness Module

**Purpose**: Enable AI to know who it is and what it's doing.

**Key Components**:
- `Identity`: AI's self-concept
- `CurrentState`: What the AI is doing now
- `Intention`: Why the AI is doing something

**API**:
```python
from claw_cog import SelfAwareness

awareness = SelfAwareness()
identity = awareness.get_identity()
state = awareness.get_current_state()
intention = awareness.get_intention()
```

### 2. Reflective Reasoning Module

**Purpose**: Enable AI to reflect on its behaviors and decisions.

**Key Components**:
- `Action`: Represents an action taken
- `Outcome`: Result of an action
- `Reflection`: Analysis of action-outcome pair
- `MetaReasoning`: Metacognitive analysis

**API**:
```python
from claw_cog import ReflectiveReasoning

reflection = ReflectiveReasoning()
result = reflection.reflect_on_action(action, outcome)
meta = reflection.meta_reasoning(problem)
```

### 3. Goal-Driven Module

**Purpose**: Enable AI to set and pursue goals autonomously.

**Key Components**:
- `Goal`: Represents a goal
- `Progress`: Progress tracking
- `GoalDriven`: Goal management system

**API**:
```python
from claw_cog import GoalDriven

goals = GoalDriven()
goal = goals.set_goal("Complete the project")
progress = goals.evaluate_progress()
```

### 4. Boundary Cognition Module

**Purpose**: Enable AI to understand its capabilities and ethical limits.

**Key Components**:
- `Boundary`: Represents a boundary
- `BoundaryCognition`: Boundary management

**API**:
```python
from claw_cog import BoundaryCognition

boundaries = BoundaryCognition()
can_do = boundaries.check_capability(action)
should_do = boundaries.check_ethical(action)
```

## Integration with claw-mem and claw-rl

### Memory Integration

claw-cog uses claw-mem for:
- Storing reflections and lessons learned
- Persisting goal history
- Remembering identity and context

### Learning Integration

claw-cog uses claw-rl for:
- Improving reflection quality over time
- Optimizing goal strategies
- Learning from past actions

## Design Principles

1. **Separation of Concerns**: Each module handles one aspect of cognition
2. **Provider Pattern**: Support multiple memory/learning providers
3. **Immutability**: Core data structures are immutable
4. **Type Safety**: Full type annotations for all public APIs

## Performance Considerations

- Minimal overhead: <5ms for basic operations
- Lazy loading: Load resources only when needed
- Caching: Cache frequently used identity/state

## Extension Points

1. **Custom Memory Providers**: Implement provider interface
2. **Custom Learning Providers**: Implement provider interface
3. **Custom Reflection Strategies**: Extend ReflectiveReasoning
4. **Custom Goal Decomposition**: Extend GoalDriven

## Future Enhancements

- Vector-based similarity search for reflections
- Reinforcement learning for goal prioritization
- Multi-agent cognition coordination
- Emotion and personality modeling
