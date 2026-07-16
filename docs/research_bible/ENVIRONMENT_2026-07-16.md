# Environment — Final Validated State (2026-07-16)

**Purpose:** The single, current statement of which Python installation and package versions this project's notebooks/tests/scripts were last confirmed to run against, and how to reproduce it. Complements — does not replace — `requirements.txt`/`requirements-dev.txt`/`requirements-lock.txt`, which remain the source of truth for exact pins and are not overwritten by this document.
**Added:** 2026-07-16, repository finalisation pass.

## Supported Python version

**Python 3.14.x**, confirmed at **3.14.6**.

## Final validation Python executable

`/usr/local/bin/python3` — **not** the platform-default `python3` (`/opt/homebrew/bin/python3.14` on the machine this project was developed on). The default install's `numpy` is broken (`ModuleNotFoundError: No module named 'numpy'`, confirmed 2026-07-15 and re-confirmed 2026-07-16); a separate, complete install at `/usr/local/bin/python3` is the one all live notebook executions, test runs, and this finalisation pass's validation checks actually used. On any new machine, `python -m venv venv` from a known-good Python 3.14 interpreter (§ below) avoids this issue entirely — it is a quirk of one specific development machine, not a project requirement.

## Package versions (confirmed installed and working, 2026-07-16)

| Package | Installed | Pinned in `requirements.txt` |
|---|---|---|
| numpy | 2.4.6 | 2.5.1 |
| pandas | 3.0.3 | 3.0.3 |
| scipy | 1.18.0 | 1.18.0 |
| scikit-learn | 1.9.0 | 1.9.0 |
| xgboost | 3.3.0 | 3.3.0 |
| lightgbm | 4.6.0 | 4.6.0 |
| dowhy | 0.8 | 0.8 |
| statsmodels | 0.14.6 | 0.14.6 |
| pyarrow | 25.0.0 | 25.0.0 |
| matplotlib | 3.11.0 | 3.11.0 |
| pytest | 9.1.1 | (in `requirements-dev.txt`, unpinned) |

Only `numpy` differs from `requirements.txt`'s pin (2.4.6 installed vs. 2.5.1 pinned) — this reflects when each package was last installed on the validation machine, not a known incompatibility; no test or notebook failure has been attributed to this difference. `requirements-lock.txt` (160 lines, full transitive closure) is the authoritative record of a complete working install and is not reproduced here.

## Installation command

```bash
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt          # pipeline dependencies
pip install -r requirements-dev.txt       # + pytest, newsapi-python, optional SHAP
```

## Test command

```bash
python -m pytest tests/ -v
```
Expected: **18 passed** (10 `tests/test_event_study.py`, 4 `tests/test_legacy_causal_engine.py`, 4 `tests/test_features.py`). Confirmed 2026-07-16 against `/usr/local/bin/python3`, unchanged from the 2026-07-15 result recorded in `10_decision_log.md`.

## Notebook execution command

```bash
jupyter lab
# or, for a full non-interactive re-run of a single notebook (not required for normal use — see notebooks/README.md's frozen-snapshot warning):
jupyter nbconvert --to notebook --execute --inplace notebooks/0N_<name>.ipynb
```

## Known unsupported configuration

- **SHAP is guarded to `python_version < "3.14"`** in `requirements-dev.txt` — its `numba` dependency does not support Python 3.14. The canonical `07_model_evaluation.ipynb` uses native XGBoost/LightGBM contribution APIs instead and does not require SHAP to run. `src/evaluation.py`'s SHAP path is an optional legacy explainability route, not part of the frozen RQ2/RQ3 evidence chain.
- **The platform-default `python3` on the development machine has a broken `numpy` install** (see above) — do not assume `python3` on any given machine is the right interpreter without checking.

## Platform notes

Developed and validated on macOS (Apple Silicon). `torch`/`transformers` (FinBERT) will use MPS acceleration if available, falling back to CPU. No platform-specific code paths are known to affect Linux/Windows, but only macOS has been exercised.

## External services

Notebook 01 calls live external APIs: Yahoo Finance (`yfinance`, keyless), the American Presidency Project (keyless), the Federal Reserve's FOMC calendar (keyless), FRED (`fredapi`, optional key), and GDELT (keyless). None of these are required to reproduce any reported result — see `notebooks/README.md`'s external-data warning; every downstream notebook reads only the already-frozen `data/raw/`/`data/processed/` parquet files checked into the local (gitignored) working tree.

## Local-only dependencies

`config.yaml` (API keys/parameters) and `notebooks/.env` (Hugging Face token, other credentials) are both required only for a genuine from-scratch Notebook 01 re-run and are both gitignored — see the root `README.md`'s Data Availability section. No secret or credential from either file is required to read, test, or validate any already-frozen artefact in this repository.

## Portability statement

This project is **not** fully portable out of the box: Notebook 01 requires live external network access and (optionally) API keys for a genuine from-scratch data pull, and several large local-only artefacts (raw/processed data, trained models) are gitignored and must either be reproduced by running Notebooks 01–07 in order or obtained from the project owner directly. Code, notebooks (with their saved outputs and figures), tests, and all documentation are fully portable and require no external service to read or inspect.
