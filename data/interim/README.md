# data/interim/

**Updated 2026-07-13** — this folder is currently **empty** (only `.gitkeep`) in the implemented pipeline. The previous version of this README described a `02_data_cleaning.ipynb` staging step — no such notebook exists; the actual `02_eda.ipynb` performs exploratory analysis only, and Notebooks 01/03/04/05 each write directly from raw inputs to their `data/processed/` outputs with no intermediate staging file. This mirrors `data/external/README.md`'s "reserved but unused" framing for the same reason: an early scaffolding placeholder from before the pipeline's actual notebook structure was settled.

Nothing in this directory is committed to git (see root `.gitignore`); if a genuine multi-step transformation ever needs an inspectable intermediate checkpoint, it belongs here — until then, this folder is reserved but unused.

**Input:** n/a (unused). **Output:** n/a (unused). **Dependencies:** none currently.
