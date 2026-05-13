# Indicator Properties

claw-cog tracks five falsifiable consciousness indicators from Butlin et al. These indicators provide a quantitative framework for evaluating whether an AI system exhibits properties consistent with conscious processing.

---

## Overview

| Theory | Indicator | v1.0.0rc2 | Sub-properties |
|--------|-----------|:---------:|----------------|
| **GWT** | Global Workspace Theory | ✅ | — |
| **RPT** | Recurrent Processing Theory | ✅ | feedback_loops, temporal_integration, hierarchical_processing |
| **HOT** | Higher-Order Thought Theory | ✅ | higher_order_representation, meta_monitoring, self_awareness, introspection |
| **AST** | Attention Schema Theory | ✅ | attention_schema, precision_weighting, resource_allocation |
| **PP** | Perceptual Presence | v2.0.0 | — |

---

## GWT — Global Workspace Theory

**Origin:** Baars (1988), Dehaene (2014)

**Claim:** Consciousness arises from a global workspace that broadcasts selected information to specialized processors.

**claw-cog implementation:**
- `GlobalWorkspace` with subscriber-based broadcast
- Information integration from multiple unconscious sources
- Default baseline subscriber ensures confidence > 0

**Status:** ✅ Full implementation

---

## RPT — Recurrent Processing Theory

**Origin:** Lamme (2006)

**Claim:** Consciousness requires recurrent (feedback) processing between brain regions, not just feedforward activation.

**claw-cog implementation:**

| Sub-property | Status | Description |
|--------------|:------:|-------------|
| `recurrent_processing` | ✅ | Always active |
| `feedback_loops` | ✅ | C0→C1→C2 layer pipeline with C2 adjustment |
| `temporal_integration` | ✅ | Memory retrieval injects past context |
| `hierarchical_processing` | ✅ | Three-layer architecture (C0→C1→C2) |

**Coverage:** 100% (4/4)

---

## HOT — Higher-Order Thought Theory

**Origin:** Rosenthal (2005)

**Claim:** A mental state is conscious when one has a higher-order thought about that state.

**claw-cog implementation:**

| Sub-property | Status | Description |
|--------------|:------:|-------------|
| `higher_order_representation` | ✅ | C2 monitors C1 output |
| `meta_monitoring` | ✅ | Metacognitive confidence assessment |
| `self_awareness` | ✅ | Competence assessment via MUSE framework |
| `introspection` | ✅ | Performance trend analysis in C2 |

**Coverage:** 100% with C2 enabled, 0% when disabled

---

## AST — Attention Schema Theory

**Origin:** Graziano (2013)

**Claim:** Consciousness is the brain's simplified model (schema) of its own attention process.

**claw-cog implementation:**

| Sub-property | Status | Description |
|--------------|:------:|-------------|
| `attention_schema` | ✅ | Workspace subscriber/attention mechanism |
| `precision_weighting` | ✅ | Weighted integration based on source confidence |
| `resource_allocation` | ✅ | Subscriber count management + batch optimization |

**Coverage:** 100% (3/3)

---

## PP — Perceptual Presence

**Origin:** Seth (2021)

**Claim:** Conscious perception involves predictive processing with counterfactual richness.

**claw-cog status:** Deferred to v2.0.0

**Coverage:** 0%

---

## Using Indicator Properties

### Check all indicators

```python
from claw_cog import ConsciousAgent

agent = ConsciousAgent()
indicators = agent.get_indicator_properties()

# RPT sub-properties
print(indicators["RPT"]["feedback_loops"])    # True
print(indicators["RPT"]["temporal_integration"]) # True

# HOT sub-properties
print(indicators["HOT"]["meta_monitoring"])    # True

# AST sub-properties
print(indicators["AST"]["precision_weighting"]) # True
```

### Get coverage scores

```python
scores = agent.get_indicator_scores()
# {"GWT": 1.0, "RPT": 1.0, "HOT": 1.0, "PP": 0.0, "AST": 1.0}
```

### Overall indicator coverage

```python
avg = sum(scores.values()) / len(scores)  # 0.80 (4/5)
```

---

## Notes

- **GWT** and **PP** are simple boolean indicators (implemented or not)
- **RPT**, **HOT**, and **AST** include detailed sub-property assessments (rc.2)
- **PP** (Perceptual Presence) is planned for v2.0.0
- Indicator properties are computed dynamically based on current agent state
