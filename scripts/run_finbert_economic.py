"""
run_finbert_economic.py — FinBERT scorer for the Notebook 01 "economic" APP subset
====================================================================================
Runs OUTSIDE Jupyter so the notebook kernel never freezes.

Scores `data/raw/app_presidential_documents_economic.parquet` (the 916-document
economic pre-filter produced by 01_data_collection.ipynb) using the project's own
src/event_detector.py::EventDetector, which implements the frozen FinBERT scoring
contract documented in dissertation Table 2 (batch size 32, max sequence length 512,
minimum acceptance confidence 0.70 top-class).

Output is written to data/raw/app_finbert_sentiment_cache.parquet, the first
candidate path checked by 03_event_detection_revised.ipynb's FinBERT cache loader.

Usage:
    python3 scripts/run_finbert_economic.py
"""

import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from src.event_detector import EventDetector

RAW = ROOT / "data" / "raw"
SRC_PATH = RAW / "app_presidential_documents_economic.parquet"
OUT_PATH = RAW / "app_finbert_sentiment_cache.parquet"

print(f"Loading {SRC_PATH.name}...")
app = pd.read_parquet(SRC_PATH)
print(f"  {len(app):,} documents loaded")

detector = EventDetector(model_name="ProsusAI/finbert", batch_size=32, threshold=0.70)

print("\nLoading FinBERT (ProsusAI/finbert)... this downloads ~440MB on first run.")
t0 = time.time()
scored = detector.score_headlines(app, text_col="title")
elapsed = time.time() - t0
print(f"✓ Scored {len(scored):,} titles in {elapsed:.1f}s")

scored["sentiment_source"] = "finbert"

cache_cols = ["date", "title", "president", "doc_type", "url",
              "sentiment_label", "sentiment_score", "sentiment_numeric", "sentiment_source"]
cache = scored[cache_cols].copy()

print("\nSentiment distribution (FinBERT, 0.70 confidence threshold):")
dist = cache["sentiment_label"].value_counts()
for label, cnt in dist.items():
    print(f"  {label:10s}  {cnt:5,d}  ({100*cnt/len(cache):.1f}%)")
print(f"\n  Mean sentiment_score  : {cache['sentiment_score'].mean():.4f}")
print(f"  Mean sentiment_numeric: {cache['sentiment_numeric'].mean():.4f}")

cache.to_parquet(OUT_PATH, index=False)
print(f"\n✓ Saved {OUT_PATH.relative_to(ROOT)} ({len(cache):,} rows x {cache.shape[1]} cols)")
print("Notebook 03 will load these scores from cache automatically on next run.")
