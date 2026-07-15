# tests/

**Purpose:** Unit tests for the reusable modules in `src/`.
**Added:** 2026-07-06 (repository hygiene pass — this folder previously had no README).

## Contents

| Test file | Covers | Status |
|-----------|--------|--------|
| `test_event_study.py` | `src/event_study_reference.py` — a dependency-free reference implementation of the **actual** constant-mean-return event-study method used in `notebooks/04_causal_analysis.ipynb` (cell 6, `compute_car`) | ✅ Active methodology — cross-validated to <1e-6 against all 264 rows of the frozen `data/processed/car_results.parquet` |
| `test_legacy_causal_engine.py` | `EventStudy` class in `src/causal_engine.py` — an OLS market-model event study, not used by any current notebook | ⚠️ Legacy/unused — kept as an independent reference implementation, not a validation of any reported result |
| `test_features.py` | `FeatureEngineer` class in `src/features.py` | Reusable `src/` implementation, predates FES v1.1 |

**2026-07-15 correction:** `test_event_study.py` previously tested `src/causal_engine.py::EventStudy`, which `docs/research_bible/03_methodology.md` itself flags as unused legacy code — meaning the repository's only event-study unit test validated a different methodology than the one that actually produced `car_results.parquet`. That test file was renamed to `test_legacy_causal_engine.py` (kept, clearly labelled, not deleted — it's a genuinely independent implementation of the classical OLS market-model event study). A new `test_event_study.py` was added against a new module, `src/event_study_reference.py`, which reproduces Notebook 04's real constant-mean-return calculation exactly (same estimation window (-252,-21), event window (-5,10), 60-observation minimum) without any pandas/numpy dependency. It was validated against hand-computable synthetic examples and then against every row of the frozen `car_results.parquet`, matching to floating-point precision (max abs diff ~1e-13). Notebook 04 itself was **not** refactored to import this module — the equivalence check earns the *option* to do so, but there is no functional need, and the notebook is dissertation-referenced. See `docs/research_bible/10_decision_log.md`, 2026-07-15 entry.

**Note (updated 2026-07-14):** these tests cover the reusable `src/` implementations, which predate the current FES v1.1/MCP v1.0 notebook contracts (see `src/README.md`). They do not validate the current notebook-level feature/model/figure construction in `05_feature_engineering.ipynb`–`08_results_visualisation.ipynb`; that boundary is instead checked by the notebooks' blocking validation cells and the three downstream validation JSON files under `reports/`.

## Running

```bash
pytest tests/
```

## Dependencies

`src/causal_engine.py`, `src/event_study_reference.py` (no external dependencies), `src/features.py`, `pytest`.
