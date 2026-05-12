# claw-cog Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
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
