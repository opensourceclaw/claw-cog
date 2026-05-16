# claw-cog Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2026-05-16

### Added
- **ITCMA**: Integrated Temporal Consciousness Model Architecture
- `ConsciousnessResultWithTime`: Extended result with temporal events, patterns, conflicts, and deadline alerts
- `TemporalPerception` integration at C0 level (event detection from input streams)
- `TemporalUnderstanding` integration at C1 level (pattern recognition, schedule inference, deadline awareness)
- `TemporalPrediction` integration at C2 level (future event prediction, conflict detection, resolution suggestion)
- Time-aware memory features in `ClawMemBridge`:
  - `apply_time_decay()`: Exponential time-based relevance decay
  - `search_by_time_range()`: Memory search within datetime ranges
  - `store_with_temporal()`: Store memories with timestamp metadata
  - `get_temporal_stats()`: Temporal memory statistics
- Temporal configuration fields: `temporal_enabled`, `temporal_horizon_days`, `temporal_retention_capacity`, `temporal_decay_rate`, `temporal_confidence_threshold`
- `enable_temporal` parameter on `ConsciousAgent.process()` for runtime toggle
- Temporal metrics in `ConsciousAgent.get_metrics()`
- Integration test suite (36 tests) covering full temporal pipeline

### Changed
- `ConsciousAgent.__init__`: Now initializes temporal modules by default
- `ConsciousAgent.process()`: Returns `ConsciousnessResultWithTime` when temporal enabled
- `ConsciousAgent.reset()`: Resets temporal module state
- `ConsciousAgent.get_metrics()`: Includes temporal perception/understanding/prediction stats
- `Config.to_dict()`: Includes temporal configuration fields
- `ConsciousAgent.get_indicator_properties()`: PP indicator tied to `temporal_enabled`; RPT temporal_integration reflects config
- `TemporalPerception.clear_history()`: Now resets statistics counters
- `TemporalUnderstanding.clear()`: Now resets statistics counters
- Version bumped from `1.0.0` to `1.5.0`

### Fixed
- `test_get_indicator_properties`: Updated to reflect PP=True (temporal integration)
- `test_indicator_properties_after_processing`: Updated for v1.5.0 changes

## [1.0.0rc2] - 2026-05-13

### Added
- Batch broadcast optimization in GlobalWorkspace
- Content cache for hot-broadcast reuse
- C2 sampling rate and TTL caching for monitoring performance
- Enhanced indicator properties with sub-property dicts (RPT/HOT/AST)
- `get_indicator_scores()` for numeric coverage percentages
- docs/INDICATORS.md — detailed indicator property reference

### Changed
- `get_indicator_properties()`: RPT/HOT/AST now return sub-property dicts
- QUICK_START.md updated with rc.2 indicator examples

## [1.0.0rc1] - 2026-05-13

### Notice
⚠️ **API Freeze**: From this release onward, no breaking changes will be made before v1.0.0.

### Added
- API stability commitment
- Semantic versioning guarantee

### Changed
- Version: beta.3 → release candidate.1

## [1.0.0b3] - 2026-05-13

### Added
- `generate_calibration_data()` method for meta-d' bootstrapping
- C2 monitoring: `performance_trend`, `learning_signal`, `attention_score` fields
- Trend analysis: `_analyze_trend()` for confidence trajectory
- Learning signal generation: `_generate_learning_signal()`

### Changed
- `assessment_min_samples`: 10 → 5 (lower threshold for meta-d')
- Test coverage: 91% → 93%
- Tests: 150 → 200
- agent.py coverage: 66% → 97%

### Fixed
- meta-d' evaluation now returns valid values (was 0.0)
- M-ratio calculation working

### Verified
- meta-d' = 1.0 ✅
- M-ratio = 0.22 ✅
- C2 monitoring enhanced ✅

## [1.0.0b2] - 2026-05-13

### Fixed
- **Confidence calculation**: Add default subscriber for GWT broadcast (fixes confidence=0.00 bug)
- **Memory type compatibility**: Map reflection→episodic in ClawMemBridge (fixes "Unknown memory type" warning)
- C0→C1 confidence propagation improved

### Changed
- Version bump: beta.1 → beta.2
- Integration test verified: confidence now 1.00 (was 0.00)

## [1.0.0b1] - 2026-05-13

### Changed
- Version bump: alpha.3 → beta.1
- Mark as public beta release

### Notes
- Core functionality complete and stable
- API frozen (no breaking changes before v1.0.0)
- Ready for public testing

## [1.0.0a3] - 2026-05-13
### Added
- Indicator properties test suite (RPT 5, HOT 6, AST 5 tests)
- Performance benchmarks (GWT/C0/meta-d'/end-to-end)
- Custom exceptions (ClawCogError, ConfigurationError, LayerError, WorkspaceError, AssessmentError)
- Subscriber Protocol type definition
- CLI test coverage
- Config validation and error handling

### Changed
- Coverage 80% → 91%
- Tests 84 → 114
- Type safety: replaced `Any` with concrete types
- README completely rewritten for v1.0.0 architecture
- docs/API.md: full API reference
- docs/ARCHITECTURE.md: complete architecture overview
- docs/QUICK_START.md: installation and usage guide

### Fixed
- pyproject.toml version sync with __init__.py

## [1.0.0a2] - 2026-05-12
### Added
- GlobalWorkspace weighted integration
- C0 multi-keyword pattern matching with regex auto-response triggers
- C1 memory retrieval via claw-mem bridge + Ego decision logic
- C2 MUSE competence assessment (coverage/novelty/risk/recommendation)
- meta-d' statistical significance test (permutation) + bootstrap CI
- Type-2 ROC AUC computation
- 26 new tests (total 84, coverage 80%)
### Fixed
- claw-mem bridge API (text → content)
- Legacy v0.1.0 package imports for migration
- C0 pattern matching now weighted multi-keyword scoring
### Changed
- Coverage 56% → 80%
- Tests 58 → 84

## [0.1.0] - 2026-05-09

### Added
- Initial project structure
- Core module architecture design
  - Self-awareness module
  - Reflective reasoning module
  - Goal-driven module
  - Boundary cognition module
- Integration with claw-mem and claw-rl
- Basic documentation structure

### Notes
- This is an alpha release for architecture validation
- Core functionality still under development
- API may change significantly before v1.0.0
