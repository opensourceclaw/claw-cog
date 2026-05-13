# claw-cog Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
