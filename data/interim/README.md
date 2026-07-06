# data/interim/

Intermediate artefacts produced between raw collection and final processed datasets — e.g. partially cleaned frames, merge checkpoints, or cached scrape results that are not yet the final modelling table.

Nothing in this directory is committed to git (see root `.gitignore`); everything here must be regenerable by re-running the notebooks in `notebooks/` in order.

**Purpose:** staging area for multi-step transformations in `02_data_cleaning` so intermediate state can be inspected without re-running the full pipeline.
**Contents:** none tracked — populated at runtime.
**Input:** `data/raw/`
**Output:** consumed by `data/processed/` build steps.
**Dependencies:** `notebooks/02_data_cleaning.ipynb` (or equivalent cleaning stage), `src/`.
