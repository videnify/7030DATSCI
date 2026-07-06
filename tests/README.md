# tests/

**Purpose:** Unit tests for the reusable modules in `src/`.
**Added:** 2026-07-06 (repository hygiene pass — this folder previously had no README).

## Contents

| Test file | Covers |
|-----------|--------|
| `test_event_study.py` | `EventStudy` class in `src/causal_engine.py` |
| `test_features.py` | `FeatureEngineer` class in `src/features.py` |

**Note (2026-07-06):** these tests cover the `src/` module-level implementations, which predate the frozen FES v1.0/MCP v1.0 contracts (see `src/README.md`). They verify the reusable helper logic, not the current notebook-level feature/model construction in `05_feature_engineering.ipynb`–`07_model_evaluation.ipynb`, which is validated instead by each notebook's own in-notebook reproduction-check cells (see `docs/research_bible/10_decision_log.md`, Mission 05-07 Reproducibility Rebuild).

## Running

```bash
pytest tests/
```

## Dependencies

`src/causal_engine.py`, `src/features.py`, `pytest`.
