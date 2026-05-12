# API Reference

This document covers the public API of claw-cog v1.0.0.

---

## ConsciousAgent

Main entry point. Orchestrates the C0→C1→C2 processing pipeline.

```python
from claw_cog import ConsciousAgent
```

### Constructor

```python
ConsciousAgent(
    config: Optional[Config] = None,
    enable_c2: bool = True,
    memory_backend: str = "claw-mem",
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `config` | `Config` | `Config()` | Configuration object |
| `enable_c2` | `bool` | `True` | Enable C2 metacognitive layer |
| `memory_backend` | `str` | `"claw-mem"` | Memory backend identifier |

### Methods

#### `process(input, context=None, confidence_threshold=0.7) -> ProcessingResult`

Process input through all consciousness layers.

```python
agent = ConsciousAgent()
result = agent.process("What should I do next?")
print(result.output)       # Processed output
print(result.confidence)   # Confidence score (0.0-1.0)
print(result.level)        # ConsciousnessLevel enum
print(result.metadata)     # dict with layer info
```

**Returns**: `ProcessingResult` with fields:
- `output: Any` — Final output from the pipeline
- `confidence: float` — Confidence score 0.0-1.0
- `level: ConsciousnessLevel` — C0_UNCONSCIOUS / C1_CONSCIOUS_ACCESS / C2_METACOGNITIVE
- `metadata: dict` — Layer info (`c0_contribution`, `c0_pattern`, `c2_monitoring`, `broadcast_time_ms`)

#### `get_indicator_properties() -> Dict[str, bool]`

Returns the five consciousness indicator properties (Butlin et al.):

```python
indicators = agent.get_indicator_properties()
# {"GWT": True, "RPT": True, "HOT": True, "PP": False, "AST": True}
```

#### `assess_metacognition() -> Dict[str, float]`

Evaluate metacognitive ability using the meta-d' framework. Requires at least 10 processing rounds.

```python
for i in range(15):
    agent.process(f"input {i}")

metrics = agent.assess_metacognition()
# {
#   "meta_d_prime": 0.xxx,
#   "d_prime": 0.xxx,
#   "m_ratio": 0.xxx,
#   "type2_roc_auc": 0.xxx,
#   "sample_size": 15
# }
```

#### `get_metrics() -> Dict[str, Any]`

Get performance and state metrics.

```python
metrics = agent.get_metrics()
# {"workspace": {...}, "layers": {...}, "history_size": N}
```

#### `reset()`

Clear processing history and reset layers.

---

## Config

Configuration dataclass with all tunable parameters.

```python
from claw_cog import Config

config = Config(
    # Workspace
    workspace_broadcast_timeout_ms=100,
    workspace_max_subscribers=10,

    # C0: Unconscious
    c0_pattern_threshold=0.7,
    c0_auto_response_enabled=True,

    # C1: Conscious
    c1_integration_method="weighted_average",
    c1_confidence_threshold=0.7,

    # C2: Metacognitive
    c2_enabled=True,
    c2_high_threshold=0.8,
    c2_medium_threshold=0.5,
    c2_low_threshold=0.3,

    # Assessment
    assessment_min_samples=10,
    assessment_history_size=1000,

    # Memory
    memory_backend="claw-mem",
    memory_context_max_tokens=4000,

    # Performance
    enable_profiling=False,
    log_level="INFO",
)
```

#### Class Methods

- `from_dict(data: dict) -> Config` — Create config from dictionary
- `to_dict() -> dict` — Serialize config to dictionary

---

## GlobalWorkspace

GNWT implementation — central hub for information integration and broadcast.

```python
from claw_cog import GlobalWorkspace
```

### Constructor

```python
GlobalWorkspace(config: Config)
```

### Methods

#### `subscribe(module: Callable) -> None`

Subscribe a module to receive broadcasts.

```python
def my_handler(content):
    print(f"Received: {content}")

ws = GlobalWorkspace(config)
ws.subscribe(my_handler)
```

#### `unsubscribe(module: Callable) -> None`

Remove a subscriber.

#### `process(input, c0_output, context=None) -> C1Result`

Integrate information and broadcast to subscribers.

```python
result = ws.process(
    input="user query",
    c0_output=c0_result,
    context={"memory_output": "previous context"}
)
# result.output — integrated content (highest-confidence source)
# result.confidence — integration score
# result.broadcast_time_ms — broadcast latency
```

#### `get_metrics() -> Dict[str, float]`

```python
# {"avg_broadcast_time_ms": 0.5, "total_broadcasts": 10, "subscriber_count": 3}
```

#### `is_implemented() -> bool`

Always `True` (returns GWT indicator).

#### `has_attention_mechanism() -> bool`

Always `True` (returns AST indicator).

#### `clear_history() -> None`

Clear broadcast history.

---

## LayerManager

Manages C0/C1/C2 layers and feedback loops.

```python
from claw_cog import LayerManager

lm = LayerManager(config, enable_c2=True)
```

### Attributes

- `lm.c0` — `C0Unconscious` instance
- `lm.c1` — `C1Conscious` instance
- `lm.c2` — `C2Metacognitive` instance (or `None` if disabled)
- `lm.c2_enabled` — `bool`

### Methods

#### `has_feedback_loops() -> bool`

Returns RPT indicator (always `True` in v1.0.0).

#### `get_layer_status() -> Dict[str, bool]`

```python
# {"c0_active": True, "c1_active": True, "c2_active": True}
```

#### `reset() -> None`

Reset all layers.

---

## C0Unconscious

Fast unconscious processing: auto responses, pattern matching, primal impressions.

```python
from claw_cog.layers.c0_unconscious import C0Unconscious

c0 = C0Unconscious(config)
```

### Methods

#### `process(input, context=None) -> C0Result`

```python
result = c0.process("hello world")
# result.output — matched response/impression
# result.contribution — confidence (0.3 to 0.8)
# result.pattern_matched — "auto_response" | pattern_name | "primal_impression"
# result.processing_time_ms — latency
```

#### `add_pattern(name: str, keywords: List[str]) -> None`

Register a pattern for matching with trigger keywords.

```python
c0.add_pattern("greeting", ["hello", "hi", "hey"])
```

#### `add_auto_response(trigger: str, response: Any) -> None`

Register an automatic response. Supports `regex:` prefix.

```python
c0.add_auto_response("help", "How can I assist you?")
c0.add_auto_response("regex:[0-9]+", "I see a number")
```

#### `get_pattern_count() -> int`

#### `get_metrics() -> Dict[str, Any]`

```python
# {"call_count": N, "avg_time_ms": X, "patterns_registered": Y, "auto_responses_registered": Z}
```

### C0Result

```python
@dataclass
class C0Result:
    output: Any              # Matched response or impression
    contribution: float      # 0.0-1.0
    pattern_matched: str     # Which pattern (or "primal_impression")
    processing_time_ms: float
```

---

## C2Metacognitive

Metacognitive monitoring and competence assessment.

```python
from claw_cog.layers.c2_metacognitive import C2Metacognitive

c2 = C2Metacognitive(config)
```

### Methods

#### `monitor(c1_result, confidence_threshold=0.7) -> C2Result`

Monitor C1 output and recommend adjustments.

```python
result = c2.monitor(c1_result)
# result.needs_adjustment — bool
# result.adjustment_type — "none" | "strategy" | "confidence" | "seek_help"
# result.confidence_estimate — float
# result.recommendation — str or None
```

Confidence bands:
- ≥ 0.8 → `"none"` (no adjustment needed)
- ≥ 0.5 → `"strategy"` (gather more information)
- ≥ 0.3 → `"confidence"` (increase confidence)
- < 0.3 → `"seek_help"` (request human assistance)

#### `assess_competence(situation, known_situations=None) -> CompetenceAssessment`

MUSE framework competence evaluation.

```python
assessment = c2.assess_competence(
    "new task description",
    known_situations=["similar task 1", "similar task 2"]
)
# assessment.score — overall competence 0.0-1.0
# assessment.known_coverage — ratio of known situations
# assessment.novelty_score — how new/unknown
# assessment.risk_level — "low" | "medium" | "high"
# assessment.recommendation — suggested action
```

#### `get_monitor_stats() -> Dict[str, Any]`

```python
# {"total_monitors": N, "adjustments": {...}, "trusted_ratio": X}
```

### C2Result

```python
@dataclass
class C2Result:
    needs_adjustment: bool
    adjustment_type: str          # "none" | "strategy" | "confidence" | "seek_help"
    confidence_estimate: float
    recommendation: Optional[str]
    metadata: Dict[str, Any]
```

### CompetenceAssessment

```python
@dataclass
class CompetenceAssessment:
    score: float                  # 0.0-1.0
    known_coverage: float         # 0.0-1.0
    novelty_score: float          # 0.0-1.0
    risk_level: str               # "low" | "medium" | "high"
    recommendation: str           # Suggested action
```

---

## MetacognitiveAssessment

meta-d' framework for evaluating metacognitive ability.

```python
from claw_cog.assessment.meta_d_prime import MetacognitiveAssessment

ma = MetacognitiveAssessment(config)
```

### Methods

#### `compute_metrics(history, ground_truth=None) -> Dict[str, float]`

```python
metrics = ma.compute_metrics(history, ground_truth=[True, False, ...])
# {
#   "meta_d_prime": 0.xxx,
#   "d_prime": 0.xxx,
#   "m_ratio": 0.xxx,
#   "type2_roc_auc": 0.xxx,
#   "sample_size": N
# }
```

Requires at least `assessment_min_samples` (default: 10) items. Returns a warning if insufficient.

#### `compute_significance(history, n_permutations=1000) -> Dict[str, Any]`

Statistical significance test using permutation.

```python
result = ma.compute_significance(history)
# {"p_value": 0.xxx, "significant": True/False, "ci_95": (low, high), ...}
```

---

## Data Classes

### ProcessingResult

```python
@dataclass
class ProcessingResult:
    output: Any
    confidence: float
    level: ConsciousnessLevel
    metadata: Dict[str, Any]
```

### ConsciousnessLevel

```python
class ConsciousnessLevel(Enum):
    C0_UNCONSCIOUS = 0        # confidence ≤ 0.5
    C1_CONSCIOUS_ACCESS = 1   # 0.5 < confidence ≤ 0.8
    C2_METACOGNITIVE = 2      # confidence > 0.8
```

### C1Result

```python
@dataclass
class C1Result:
    output: Any
    confidence: float
    broadcast_time_ms: float
    metadata: Dict[str, Any]
```
