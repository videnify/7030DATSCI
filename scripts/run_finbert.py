"""
run_finbert.py — Standalone FinBERT scorer for DATSCI7030
==========================================================
Runs OUTSIDE Jupyter so the notebook kernel never freezes.
Uses M1 MPS GPU if available, falls back to CPU.

Usage:
    cd /Users/ibby/dev/LJMU/7030DATSCI-Data-Science-Project/DATSCI7030
    source ../datsci/bin/activate
    python3 scripts/run_finbert.py

Results are saved to data/processed/events_tagged.parquet.
Notebook 03 will load them from cache automatically.
"""

import os, sys, gc, time
from pathlib import Path

import torch
import pandas as pd
from tqdm import tqdm
from transformers import pipeline as hf_pipeline

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT      = Path(__file__).resolve().parent.parent
RAW       = ROOT / 'data' / 'raw'
PROCESSED = ROOT / 'data' / 'processed'
PROCESSED.mkdir(parents=True, exist_ok=True)

# ── Device ─────────────────────────────────────────────────────────────────────
if torch.backends.mps.is_available():
    DEVICE     = 'mps'
    BATCH_SIZE = 64       # conservative for 16GB RAM
    print(f'✓ M1 GPU (MPS) available — using GPU with batch_size={BATCH_SIZE}')
else:
    DEVICE     = -1       # CPU
    BATCH_SIZE = 32
    print(f'⚠ MPS not available — using CPU with batch_size={BATCH_SIZE}')

# ── Load APP documents ─────────────────────────────────────────────────────────
print('\nLoading APP presidential documents...')
app = pd.read_parquet(RAW / 'app_presidential_documents.parquet')
CORE_PRESIDENTS = [
    'Barack Obama',
    'Donald J. Trump (1st Term)',
    'Joseph R. Biden, Jr.',
    'Donald J. Trump (2nd Term)',
]
app = app[app['president'].isin(CORE_PRESIDENTS)].copy()
app['date']  = pd.to_datetime(app['date']).dt.normalize()
app['title'] = app['title'].fillna('').str.strip()
print(f'  {len(app):,} documents loaded')

# ── Check cache ────────────────────────────────────────────────────────────────
cache_path = PROCESSED / 'events_tagged.parquet'
if cache_path.exists():
    cached = pd.read_parquet(cache_path)
    if 'sentiment_source' in cached.columns:
        already_finbert = (cached['sentiment_source'] == 'finbert').all()
        if already_finbert:
            print('\n✓ events_tagged.parquet already has FinBERT scores — nothing to do.')
            print('  Delete data/processed/events_tagged.parquet to force re-scoring.')
            sys.exit(0)

# ── Load FinBERT ───────────────────────────────────────────────────────────────
print('\nLoading FinBERT (ProsusAI/finbert)...')
print('  This downloads ~440MB on first run.')
t0 = time.time()

finbert = hf_pipeline(
    'text-classification',
    model='ProsusAI/finbert',
    tokenizer='ProsusAI/finbert',
    top_k=None,
    device=DEVICE,
)
print(f'✓ FinBERT loaded in {time.time()-t0:.1f}s')

# ── Score documents ────────────────────────────────────────────────────────────
titles     = app['title'].tolist()
n          = len(titles)
all_labels = []
all_scores = []

print(f'\nScoring {n:,} documents in batches of {BATCH_SIZE}...')
print('Progress is shown below. Safe to leave running.\n')

t1 = time.time()
for i in tqdm(range(0, n, BATCH_SIZE), desc='FinBERT', unit='batch'):
    batch = titles[i:i + BATCH_SIZE]
    try:
        results = finbert(batch, truncation=True, max_length=128)
        for result in results:
            top = max(result, key=lambda x: x['score'])
            all_labels.append(top['label'].lower())
            all_scores.append(round(top['score'], 4))
    except Exception as e:
        # On error, fall back to neutral for this batch
        print(f'\n  ⚠ Batch {i//BATCH_SIZE} failed: {e} — marking as neutral')
        all_labels.extend(['neutral'] * len(batch))
        all_scores.extend([0.5] * len(batch))

    # Free MPS cache every 50 batches to avoid memory creep
    if DEVICE == 'mps' and i % (50 * BATCH_SIZE) == 0 and i > 0:
        gc.collect()
        torch.mps.empty_cache()

elapsed = time.time() - t1
print(f'\n✓ Scoring complete in {elapsed/60:.1f} minutes')

# ── Attach scores ──────────────────────────────────────────────────────────────
SENTIMENT_MAP = {'positive': 1, 'negative': -1, 'neutral': 0}
app['sentiment_label']   = all_labels
app['sentiment_score']   = all_scores
app['sentiment_source']  = 'finbert'
app['sentiment_numeric'] = app['sentiment_label'].map(SENTIMENT_MAP)

# ── Distribution ───────────────────────────────────────────────────────────────
print('\nSentiment distribution (finbert):')
for label, cnt in app['sentiment_label'].value_counts().items():
    print(f'  {label:10s}  {cnt:6,d}  ({100*cnt/len(app):.1f}%)')
print(f'\n  Mean score   : {app["sentiment_score"].mean():.4f}')
print(f'  Mean numeric : {app["sentiment_numeric"].mean():.4f}')

# ── Save — merge with existing parquet if it exists ───────────────────────────
print(f'\nSaving to {cache_path}...')
if cache_path.exists():
    existing = pd.read_parquet(cache_path)
    # Drop old sentiment cols if present, merge fresh scores
    drop_cols = ['sentiment_label','sentiment_score','sentiment_source','sentiment_numeric']
    existing  = existing.drop(columns=[c for c in drop_cols if c in existing.columns])
    merged    = existing.merge(
        app[['title','sentiment_label','sentiment_score','sentiment_source','sentiment_numeric']],
        on='title', how='left'
    )
    merged.to_parquet(cache_path, index=False)
    print(f'✓ Merged FinBERT scores into existing events_tagged.parquet ({len(merged):,} rows)')
else:
    app.to_parquet(cache_path, index=False)
    print(f'✓ Saved events_tagged.parquet ({len(app):,} rows)')

print('\nDone. Re-run notebook 03 — it will load FinBERT scores from cache instantly.')
