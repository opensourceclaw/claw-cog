# Architecture Overview

claw-cog v1.0.0 implements three core cognitive neuroscience theories: **Global Workspace Theory** (GNWT), **C0-C1-C2 Layered Architecture**, and **meta-d' Metacognition**.

---

## Theoretical Foundation

### Global Workspace Theory (GNWT)

Proposed by Baars (1988) and refined by Dehaene (2014), GNWT posits that consciousness arises from a global workspace that:
- Receives input from specialized unconscious processors
- **Broadcasts** selected information to the entire system
- Enables **global access** — any module can use the information

### C0-C1-C2 Architecture

Dehaene's three-level framework:

| Level | Name | Function | Analogous to |
|-------|------|----------|-------------|
| **C0** | Unconscious | Automatic processing, pattern recognition | Freud's Id |
| **C1** | Conscious Access | Global availability, integration | Freud's Ego |
| **C2** | Metacognitive | Self-monitoring, confidence assessment | Freud's Superego |

### meta-d' Framework

Maniscalco & Lau's SDT-based method for measuring metacognitive sensitivity — the ability to distinguish correct from incorrect decisions using confidence ratings.

---

## System Architecture

```
                        ┌─────────────────────┐
                        │   ConsciousAgent     │
                        │   (Orchestrator)     │
                        └──────────┬──────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
    ┌─────▼─────┐          ┌──────▼──────┐         ┌───────▼───────┐
    │  Layer    │          │   Global    │         │ Metacognitive │
    │  Manager  │          │  Workspace  │         │  Assessment   │
    └─────┬─────┘          └──────┬──────┘         └───────────────┘
          │                       │
    ┌─────┼─────────────┐         │
    │     │             │         │
┌───▼──┐ ┌▼────┐  ┌─────▼──┐     │
│  C0  │ │ C1  │  │   C2   │     │
└──────┘ └─────┘  └────────┘     │
          │                       │
    ┌─────▼─────┐                 │
    │ claw-mem  │◄────────────────┘
    │  Bridge   │
    └───────────┘
```

---

## Processing Pipeline

```
Input
  │
  ▼
[Mempry Retrieval] → claw-mem search → inject into context
  │
  ▼
[C0: Unconscious]  → auto-response → pattern match → primal impression
  │                   contribution: 0.8 | varies | 0.3
  ▼
[C1: Workspace]    → integrate(input, C0, memory, ego) → broadcast
  │                   weighted by confidence scores
  ▼
[C2: Metacog.]     → monitor confidence level:
  │                   ≥0.8 → none (trusted)
  │                   ≥0.5 → strategy adjustment
  │                   ≥0.3 → confidence adjustment
  │                   <0.3 → seek_help
  ▼
[Build Result]     → ProcessingResult(output, confidence, level, metadata)
  │
  ▼
[Record History]   → append for metacognitive assessment
```

---

## Component Details

### C0: Unconscious Layer

Three-stage fast processing:

1. **Auto Response** — Exact/prefix/regex triggers → contribution 0.8
2. **Pattern Matching** — Multi-keyword weighted scoring → score = min(1.0, matched/total × 0.8 + 0.2)
3. **Primal Impression** — Extract key features as fallback → contribution 0.3

### C1: Global Workspace

- **Integration** — Weighted combination: input(0.3) + C0(varies) + memory(0.8) + ego(0.7)
- **Broadcast** — Notify all subscribers, compute integration score
- **Subscriber Limit** — Configurable max via `workspace_max_subscribers`

### C2: Metacognitive Layer

- **Confidence Monitor** — Four-band escalation
- **Competence Assessment** — MUSE framework (known coverage, novelty, risk)
- **Adjustment Types** — `none`, `strategy`, `confidence`, `seek_help`

### Metacognitive Assessment

- **d'** — Type-1 sensitivity (task performance)
- **meta-d'** — Type-2 sensitivity (metacognitive ability)
- **M-ratio** — Metacognitive efficiency (~1.0 optimal)
- **Type-2 ROC AUC** — Discrimination of correct vs. incorrect

---

## Indicator Properties

From Butlin et al., five falsifiable indicators for AI consciousness:

| Theory | Indicator | v1.0.0 | Implementation |
|--------|-----------|:------:|----------------|
| GWT | Global Workspace Theory | ✅ | `GlobalWorkspace` with subscriber broadcast |
| RPT | Recurrent Processing Theory | ✅ | C0→C1→C2 feedback loop with adjustment |
| HOT | Higher-Order Thought Theory | ✅ | C2 metacognitive monitoring |
| AST | Attention Schema Theory | ✅ | Workspace subscriber/attention mechanism |
| PP | Perceptual Presence | v2.0.0 | Planned sensory integration |

---

## Memory Integration

`ClawMemBridge` connects to [claw-mem](https://github.com/opensourceclaw/claw-mem):

- **Retrieve** — Relevant memories injected as context
- **Store** — Reflections when C2 detects adjustment needs
- **Format** — Context-aware token budgeting

---

## Configuration

Centralized in the `Config` dataclass:

| Category | Setting | Default |
|----------|---------|---------|
| Workspace | `workspace_broadcast_timeout_ms` | 100 |
| Workspace | `workspace_max_subscribers` | 10 |
| C0 | `c0_pattern_threshold` | 0.7 |
| C0 | `c0_auto_response_enabled` | True |
| C1 | `c1_confidence_threshold` | 0.7 |
| C2 | `c2_enabled` | True |
| C2 | `c2_high/medium/low_threshold` | 0.8 / 0.5 / 0.3 |
| Assessment | `assessment_min_samples` | 10 |
| Assessment | `assessment_history_size` | 1000 |

---

## Design Decisions

1. **GNWT over competing theories** — Strongest empirical support, clear engineering mapping
2. **C0-C1-C2 as implementation framework** — Concrete, testable layered architecture
3. **meta-d' as metacognition standard** — Quantitative, signal-detection-based benchmarks
4. **Subscriber pattern for workspace** — Matches GNWT's "global availability" concept
5. **Butlin indicators as coverage metric** — Falsifiable evaluation criteria

---

## See Also

- [API Reference](API.md) — Complete API documentation
- [Quick Start](QUICK_START.md) — Getting started guide
- [V1 Architecture Design](architecture/V1_ARCHITECTURE.md) — Detailed design with pseudocode
- [Version Roadmap](VERSION_ROADMAP.md) — Release planning
