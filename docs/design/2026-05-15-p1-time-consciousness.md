# P1-2: Time Consciousness Enhancement

**Version**: v1.5.0 Target
**Priority**: P1
**Created**: 2026-05-15
**Author**: Friday (Architecture Design)

---

## 1. Problem Statement

### Current Situation
- Basic time awareness in claw-cog C0-C1-C2
- No sophisticated temporal reasoning
- Limited time-based predictions

### Target State
- Enhanced ITCMA (Integrated Temporal Consciousness Model Architecture)
- Time-based predictions and scheduling
- Temporal decay with awareness

---

## 2. Solution Overview

### ITCMA Enhancement Architecture

```
Time Input (Events/Tasks)
    │
    ▼
┌─────────────────────────────────────┐
│  Temporal Perception (C0)            │
│  - Event detection                   │
│  - Duration estimation               │
│  - Sequence recognition              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Temporal Understanding (C1)         │
│  - Pattern recognition               │
│  - Schedule inference                │
│  - Deadline awareness                │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Temporal Prediction (C2)            │
│  - Future event prediction           │
│  - Resource allocation               │
│  - Conflict detection                │
└──────────────┬──────────────────────┘
               │
               ▼
        Time-Aware Actions
```

---

## 3. Architecture Design

### 3.1 Temporal Perception (C0 Enhancement)

```python
class TemporalPerception:
    """C0: Enhanced temporal perception"""
    
    def detect_events(self, input_stream) -> List[TemporalEvent]:
        """
        Detect temporal events from input.
        
        Event types:
        - Instantaneous: single moment (e.g., "now")
        - Duration: time span (e.g., "2 hours")
        - Recurring: repeated (e.g., "every day")
        - Deadline: future point (e.g., "by Friday")
        """
        events = []
        
        for item in input_stream:
            detected = self._detect_time_expression(item)
            if detected:
                events.append(TemporalEvent(
                    type=detected.type,
                    reference=detected.reference,
                    duration=detected.duration,
                    recurrence=detected.recurrence
                ))
        
        return events
    
    def estimate_duration(self, task: Task) -> DurationEstimate:
        """Estimate task duration based on historical data"""
        # Use past experience to estimate
        similar_tasks = self.memory.search_similar(task)
        
        if similar_tasks:
            avg_duration = sum(t.duration for t in similar_tasks) / len(similar_tasks)
            confidence = len(similar_tasks) / 10  # More data = higher confidence
        else:
            # Use default estimation
            avg_duration = self._default_estimate(task.type)
            confidence = 0.3
        
        return DurationEstimate(
            expected=avg_duration,
            confidence=confidence,
            range=(avg_duration * 0.8, avg_duration * 1.2)
        )
```

### 3.2 Temporal Understanding (C1 Enhancement)

```python
class TemporalUnderstanding:
    """C1: Temporal pattern understanding"""
    
    def recognize_patterns(self, events: List[TemporalEvent]) -> List[TemporalPattern]:
        """
        Recognize temporal patterns.
        
        Patterns:
        - Daily: "every morning"
        - Weekly: "every Monday"
        - Monthly: "every month end"
        - Seasonal: "every summer"
        - Custom: "every 3 days"
        """
        patterns = []
        
        # Group events by recurrence
        groups = self._group_by_recurrence(events)
        
        for group in groups:
            pattern = TemporalPattern(
                type=self._classify_pattern(group),
                frequency=self._compute_frequency(group),
                confidence=self._compute_confidence(group)
            )
            patterns.append(pattern)
        
        return patterns
    
    def infer_schedule(self, patterns: List[TemporalPattern]) -> Schedule:
        """Infer optimal schedule from patterns"""
        # Compute optimal timing based on patterns
        # Consider: user preferences, resource constraints, conflicts
        
        schedule = Schedule()
        
        for pattern in patterns:
            optimal_time = self._find_optimal_time(pattern)
            schedule.add(
                pattern=pattern,
                suggested_time=optimal_time,
                flexibility=self._compute_flexibility(pattern)
            )
        
        return schedule
```

### 3.3 Temporal Prediction (C2 Enhancement)

```python
class TemporalPrediction:
    """C2: Temporal prediction and planning"""
    
    def predict_future_events(
        self, 
        patterns: List[TemporalPattern],
        horizon: timedelta
    ) -> List[PredictedEvent]:
        """
        Predict future events within horizon.
        
        Use patterns to predict:
        - Recurring events (from patterns)
        - Deadline events (from tasks)
        - Resource needs (from history)
        """
        predictions = []
        
        for pattern in patterns:
            # Predict next occurrences
            next_times = self._predict_next(pattern, horizon)
            
            for time in next_times:
                predictions.append(PredictedEvent(
                    pattern=pattern,
                    predicted_time=time,
                    confidence=pattern.confidence,
                    resource_need=self._estimate_resource(pattern)
                ))
        
        return predictions
    
    def detect_conflicts(
        self, 
        predictions: List[PredictedEvent],
        existing_schedule: Schedule
    ) -> List[TemporalConflict]:
        """
        Detect temporal conflicts.
        
        Conflicts:
        - Overlap: two events at same time
        - Resource: insufficient resources
        - Deadline: cannot meet deadline
        """
        conflicts = []
        
        for prediction in predictions:
            # Check overlap with existing
            overlapping = existing_schedule.check_overlap(
                prediction.predicted_time,
                prediction.duration
            )
            
            if overlapping:
                conflicts.append(TemporalConflict(
                    type="overlap",
                    events=[prediction, overlapping],
                    severity=self._compute_severity(prediction, overlapping)
                ))
            
            # Check resource availability
            if not self._check_resources(prediction):
                conflicts.append(TemporalConflict(
                    type="resource",
                    event=prediction,
                    severity="medium"
                ))
        
        return conflicts
    
    def suggest_resolution(
        self, 
        conflicts: List[TemporalConflict]
    ) -> List[ResolutionSuggestion]:
        """Suggest conflict resolution strategies"""
        suggestions = []
        
        for conflict in conflicts:
            if conflict.type == "overlap":
                # Suggest rescheduling
                alternatives = self._find_alternative_times(conflict)
                suggestions.append(ResolutionSuggestion(
                    conflict=conflict,
                    strategy="reschedule",
                    alternatives=alternatives
                ))
            
            elif conflict.type == "resource":
                # Suggest resource allocation
                suggestions.append(ResolutionSuggestion(
                    conflict=conflict,
                    strategy="allocate",
                    details=self._suggest_allocation(conflict)
                ))
        
        return suggestions
```

---

## 4. Integration with claw-cog

### 4.1 Consciousness Layer Integration

```python
class ConsciousAgentWithTime:
    """ConsciousAgent with enhanced temporal awareness"""
    
    def __init__(self):
        self.c0 = TemporalPerception()
        self.c1 = TemporalUnderstanding()
        self.c2 = TemporalPrediction()
    
    def process_with_time(
        self, 
        input: Input,
        context: Context
    ) -> ConsciousResultWithTime:
        """
        Process input with temporal awareness.
        
        C0 → C1 → C2 → Result
        """
        # C0: Detect events
        events = self.c0.detect_events(input)
        
        # C1: Understand patterns
        patterns = self.c1.recognize_patterns(events)
        schedule = self.c1.infer_schedule(patterns)
        
        # C2: Predict and detect conflicts
        predictions = self.c2.predict_future_events(
            patterns,
            horizon=timedelta(days=7)
        )
        conflicts = self.c2.detect_conflicts(predictions, schedule)
        resolutions = self.c2.suggest_resolution(conflicts)
        
        return ConsciousResultWithTime(
            events=events,
            patterns=patterns,
            schedule=schedule,
            predictions=predictions,
            conflicts=conflicts,
            resolutions=resolutions
        )
```

### 4.2 Memory Integration

```python
class TimeAwareMemory:
    """Memory with temporal awareness"""
    
    def store_with_time(
        self, 
        memory: Memory,
        temporal_context: TemporalContext
    ):
        """Store memory with temporal metadata"""
        memory.metadata["temporal"] = {
            "timestamp": temporal_context.timestamp,
            "duration": temporal_context.duration,
            "recurrence": temporal_context.recurrence,
            "deadline": temporal_context.deadline
        }
        self.memory_store.store(memory)
    
    def search_by_time(
        self, 
        time_range: TimeRange,
        filters: dict = None
    ) -> List[Memory]:
        """Search memories by time range"""
        return self.memory_store.search(
            filters={
                "timestamp": time_range,
                **(filters or {})
            }
        )
    
    def get_time_decay_weight(
        self, 
        memory: Memory,
        current_time: datetime
    ) -> float:
        """Compute time decay weight"""
        age = current_time - memory.metadata["temporal"]["timestamp"]
        
        # Decay function: exponential
        decay_rate = 0.1  # per day
        weight = math.exp(-decay_rate * age.days)
        
        return weight
```

---

## 5. Implementation Plan

### Phase 1: Temporal Perception (Week 1)
- [ ] Implement TemporalPerception class
- [ ] Add event detection
- [ ] Add duration estimation
- [ ] Unit tests

### Phase 2: Temporal Understanding (Week 2)
- [ ] Implement TemporalUnderstanding class
- [ ] Add pattern recognition
- [ ] Add schedule inference
- [ ] Unit tests

### Phase 3: Temporal Prediction (Week 3)
- [ ] Implement TemporalPrediction class
- [ ] Add future event prediction
- [ ] Add conflict detection
- [ ] Add resolution suggestion
- [ ] Integration tests

### Phase 4: Integration (Week 4)
- [ ] Integrate with claw-cog
- [ ] Integrate with claw-mem
- [ ] Performance optimization
- [ ] Documentation

---

## 6. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Pattern Recognition | > 80% | Pattern detection accuracy |
| Duration Estimation | ±20% | Estimation error |
| Conflict Detection | > 90% | Conflict detection rate |
| Resolution Quality | > 70% | Resolution acceptance rate |

---

*Architecture Design by Friday AI*