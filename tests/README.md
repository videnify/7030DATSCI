# tests/

**Purpose:** Unit tests for the reusable modules in `src/`.
**Added:** 2026-07-06 (repository hygiene pass — this folder previously had no README).

## Contents

| Test file | Covers |
|-----------|--------|
| `test_event_study.py` | `EventStudy` class in `src/causal_engine.py` |
| `test_features.py` | `FeatureEngineer` class in `src/features.py` |

**Note (updated 2026-07-14):** these tests cover the reusable `src/` implementations, which predate the current FES v1.1/MCP v1.0 notebook contracts (see `src/README.md`). They do not validate the current notebook-level feature/model/figure construction in `05_feature_engineering.ipynb`–`08_results_visualisation.ipynb`; that boundary is instead checked by the notebooks' blocking validation cells and the three downstream validation JSON files under `reports/`.

## Running

```bash
pytest tests/
```

## Dependencies

`src/causal_engine.py`, `src/features.py`, `pytest`.
