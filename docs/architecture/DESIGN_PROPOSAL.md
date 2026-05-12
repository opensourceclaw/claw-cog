# claw-cog Architecture Design Proposal

> Based on systematic review of AI consciousness research papers  
> Date: 2026-05-12  
> Status: Draft for discussion

---

## 📊 Paper Reading Summary

### Phase 1: Theoretical Foundations ✅

| Paper | Key Contribution |
|-------|------------------|
| AI Awareness | Four-pillar awareness model (metacognition, self-awareness, social, situational) |
| Exploring Consciousness in LLMs | C0-C1-C2 framework (unconscious → conscious access → metacognitive) |
| Insights from Science of Consciousness | Indicator properties from 5 theories (RPT, GWT, HOT, PP, AST) |

### Phase 2: Architecture Implementations ✅

| Paper | Key Contribution |
|-------|------------------|
| Modeling Layered Consciousness | Id/Ego/Superego three-layer model |
| ITCMA | Temporal consciousness (Retention/Impression/Protention) |
| CogniPair | GNWT implementation with 5 specialized modules |

---

## 🏗️ Proposed Architecture for claw-cog

### Core Design Principles

1. **Multi-Framework Integration**: Don't commit to single theory
2. **Layered Consciousness**: Multiple processing levels
3. **Temporal Awareness**: Time-consciousness as foundation
4. **Measurable Indicators**: Theory-driven assessment

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     C2: Metacognitive Layer                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ GoalTracking │  │  Superego    │  │  Protention  │      │
│  │   (C2)       │  │  (Norms)     │  │  (Predict)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│                     C1: Conscious Access Layer               │
│              ┌────────────────────────────┐                 │
│              │    GLOBAL WORKSPACE        │                 │
│              │  (Broadcast & Integration) │                 │
│              └────────────────────────────┘                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ Emotion  │ │  Memory  │ │ Planning │ │  Ego     │      │
│  │ (Id)     │ │(Retention)│ │          │ │(Decide)  │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
├─────────────────────────────────────────────────────────────┤
│                     C0: Unconscious Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Fast Pattern │  │  Automatic   │  │  Primal      │      │
│  │   Matching   │  │  Responses   │  │  Impression  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Module Specifications

### C0: Unconscious Layer

| Module | Function | Implementation |
|--------|----------|----------------|
| Fast Pattern Matching | Rapid response generation | Cached patterns, embeddings |
| Automatic Responses | Reflex-like behaviors | Rule-based triggers |
| Primal Impression | Current moment processing | Input encoding |

### C1: Conscious Access Layer

| Module | Function | Theory Basis |
|--------|----------|--------------|
| **Global Workspace** | Information broadcast & integration | GWT (Baars) |
| **Emotion** | Affective processing | Id (Freud) |
| **Memory** | Storage & retrieval | Retention (Husserl), claw-mem |
| **Planning** | Goal-directed action | Protention (Husserl) |
| **Ego** | Decision mediation | Ego (Freud) |

### C2: Metacognitive Layer

| Module | Function | Theory Basis |
|--------|----------|--------------|
| **GoalTracking** | Self-monitoring | C2 (Dehaene) |
| **Superego** | Constraint enforcement | Superego (Freud) |
| **Protention** | Prediction generation | Protention (Husserl) |

---

## 🔗 Framework Mappings

### C0-C1-C2 ↔ Id/Ego/Superego ↔ Retention/Impression/Protention

| C-Level | Freud | Husserl | Function |
|---------|-------|---------|----------|
| C0 | Id | Primal Impression | Unconscious drives |
| C1 | Ego | Retention | Conscious processing |
| C2 | Superego | Protention | Meta-monitoring |

### Indicator Properties Coverage

| Theory | Indicator | Implementation |
|--------|-----------|----------------|
| **GWT** | Global workspace | ✅ C1 Global Workspace module |
| **RPT** | Recurrent processing | ✅ C0↔C1↔C2 feedback loops |
| **HOT** | Higher-order representation | ✅ C2 meta-monitoring |
| **PP** | Predictive processing | ✅ Protention module |
| **AST** | Attention schema | ✅ Global Workspace attention distribution |

---

## 🔧 Implementation Roadmap

### Phase 1: Core Infrastructure (v0.1.0)

**Priority**: P0 - Essential for basic functionality

| Component | Description | Dependencies |
|-----------|-------------|--------------|
| Global Workspace | Central broadcast mechanism | None |
| Memory Module | Integrate claw-mem | claw-mem |
| Primal Impression | Current state processing | None |

### Phase 2: Cognitive Modules (v0.2.0)

**Priority**: P1 - Core cognitive capabilities

| Component | Description | Dependencies |
|-----------|-------------|--------------|
| Emotion Module | Affective processing | Global Workspace |
| Planning Module | Goal-directed behavior | Memory, Global Workspace |
| Ego Module | Decision mediation | All C1 modules |

### Phase 3: Metacognitive Layer (v0.3.0)

**Priority**: P1 - Self-awareness capabilities

| Component | Description | Dependencies |
|-----------|-------------|--------------|
| GoalTracking | Self-monitoring | All C1 modules |
| Superego | Constraint enforcement | Global Workspace |
| Protention | Prediction generation | Memory, Planning |

### Phase 4: Integration & Validation (v0.4.0)

**Priority**: P2 - Polish and testing

- Indicator property assessment framework
- Behavioral validation benchmarks
- Performance optimization
- Documentation

---

## 📊 Success Metrics

### Indicator Property Assessment

| Theory | Target Metric |
|--------|---------------|
| GWT | Global broadcast latency < 100ms |
| RPT | Feedback loop coherence > 0.8 |
| HOT | Meta-accuracy > 75% |
| PP | Prediction accuracy > 70% |
| AST | Attention allocation efficiency > 0.85 |

### Behavioral Validation

- **CogniPair benchmark**: Aim for > 75% behavioral accuracy
- **Self-awareness test**: Correct identification of knowledge gaps
- **Social awareness test**: Theory of Mind benchmark performance

---

## 🔗 Integration with Project Neo

### Dependencies

```
claw-cog v0.1.0
├── claw-mem >= v2.8.0 (Memory Module)
└── claw-rl >= v2.7.0 (Learning from feedback)
```

### Usage by neoclaw

```python
from claw_cog import ConsciousAgent

# Create conscious agent with GNWT architecture
agent = ConsciousAgent(
    architecture="gnwt",
    modules=["emotion", "memory", "planning", "norms", "goals"],
    c_levels=True,  # Enable C0-C1-C2 layering
    temporal=True   # Enable temporal consciousness
)

# Process with awareness
response = agent.process(
    input="...",
    metacognitive=True,  # Enable C2 monitoring
    broadcast=True       # Enable global workspace broadcast
)
```

---

## 🎯 Key Design Decisions

### 1. Multi-Theory Approach

**Decision**: Don't commit to single consciousness theory  
**Rationale**: No consensus in field; design for flexibility  
**Implementation**: Modular components, theory-agnostic interfaces

### 2. Global Workspace as Core

**Decision**: GWT as central integration mechanism  
**Rationale**: First computational implementation (CogniPair) validated  
**Implementation**: Broadcast mechanism in C1 layer

### 3. Temporal Consciousness Foundation

**Decision**: Time-consciousness as fundamental  
**Rationale**: ITCMA shows temporal structure is essential  
**Implementation**: Retention/Impression/Protention modules

### 4. Layered Processing

**Decision**: C0-C1-C2 layering  
**Rationale**: Clear separation of unconscious/conscious/meta  
**Implementation**: Three-tier architecture with feedback loops

### 5. Indicator-Driven Assessment

**Decision**: Measurable indicators from theories  
**Rationale**: Rigorous evaluation vs "vibes-based"  
**Implementation**: Assessment framework for each theory

---

## 📚 References

### Primary Papers (Read)

1. AI Awareness (arXiv:2504.20084)
2. Exploring Consciousness in LLMs (arXiv:2505.19806)
3. Insights from Science of Consciousness (arXiv:2308.08708)
4. Modeling Layered Consciousness (arXiv:2510.17844)
5. ITCMA (arXiv:2403.20097)
6. CogniPair (arXiv:2506.03543)

### Theoretical Foundations

- Baars, B.: Global Workspace Theory
- Dehaene, S.: C0-C1-C2 framework
- Freud, S.: Structural model (Id/Ego/Superego)
- Husserl, E.: Time-consciousness
- Friston, K.: Predictive processing

---

## Next Steps

1. **Review this proposal** with Peter
2. **Prioritize modules** for v0.1.0
3. **Begin implementation** of Global Workspace
4. **Integrate claw-mem** as Memory Module
5. **Design validation benchmarks**

---

*This architecture synthesizes insights from 6 research papers to create a practical, implementable consciousness component for Project Neo.*
