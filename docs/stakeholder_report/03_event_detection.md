# 3. Event Detection & Sentiment — Turning Raw Documents Into a Usable Signal

**Status:** ✅ Written 2026-07-15 — every number below was checked directly against the notebook's saved output and the underlying parquet files, not copied from an earlier draft.
**Originally verified:** 2026-07-13 (post-GDELT-backfill revision).
**Last reviewed against current pipeline:** 2026-07-14/15 (re-verified as part of the full eight-notebook traceability audit — no number changed as a result).
**Technical detail:** `notebooks/03_event_detection.ipynb` · [`06_feature_dictionary.md`](../research_bible/06_feature_dictionary.md) · [`10_decision_log.md`](../research_bible/10_decision_log.md) (2026-07-13 GDELT-as-continuous-confounder decision; Sentiment Engine Freeze v1.0)

---

## What this stage does

This stage turns the raw presidential documents and Fed decisions collected in Stage 1 into something a model can actually use: a single, unified catalogue of "events," each with a category (monetary, trade, geopolitical, regulatory, energy, health, labour, other) and a sentiment score, plus a daily time series of aggregated sentiment and event counts. It also folds in the global news-risk signal (GDELT) — not as a list of individual events, but as a continuous daily background reading.

## Why it matters

A raw document dump isn't useful to a predictive model. This stage decides — using explicit, documented rules — what counts as an "event," what kind of event it is, and how positive/negative/neutral its content is. Every later analysis (the event study, the causal estimate, the feature matrix) is built directly on the categorisation and sentiment scores produced here, so getting this step right (or at least being transparent about its limits) matters more than almost any other stage.

## Inputs

- 916 economically-relevant presidential documents (from Stage 1)
- 89 FOMC interest-rate decisions (from Stage 1)
- The full 2015–2025 GDELT daily geopolitical-risk summary, 4,018 days (from Stage 1)

## Outputs

- `events_tagged.parquet` — 1,005 rows (916 APP documents + 89 FOMC decisions), the unified event catalogue
- `daily_sentiment.parquet` — 739 calendar days with at least one catalogued event, plus GDELT's continuous columns merged in for every day
- `high_impact_events.parquet` — 344 rows, the "high-impact" subset used as the treatment group in the next stage
- `gdelt_daily_risk.parquet` — the standardised GDELT daily series, kept separate from the event catalogue

## What was found

- **How documents are sorted into categories:** each APP document's title/text is matched against category keyword lists. The largest group is `other` (427 of 916, 46.6%) — routine ceremonial statements and condolences with no obvious market content, which is expected. Of the market-relevant categories: trade (106), labour (103), geopolitical (96), regulatory (85), energy (64), monetary (21, mostly because monetary policy is carried by the separate FOMC channel instead), health (14, the rarest).
- **Sentiment is overwhelmingly neutral:** 869 of 916 APP documents (94.9%) score as FinBERT-neutral. This is expected for formal government communication — most titles are administrative, not overtly market-moving — but it means the *sign* of sentiment on any single event is often uninformative on its own. The causal event study (next stage) works around this by comparing abnormal returns across event *types* and a high-impact *subset*, rather than relying on individual sentiment scores.
- **FOMC decisions:** of 89 meetings, most (60, 67.4%) simply held rates — hikes (20) cluster in the 2022–2023 tightening cycle, and cuts/emergency cuts cluster around the 2020 shock and the 2024–2025 easing cycle.
- **The "high-impact" subset:** 344 of 1,005 events (34.2%) are flagged high-impact — a deliberately broad rule (high sentiment confidence, a market-relevant category, or any non-hold FOMC decision) designed to give the next stage enough observations per event type, even at the cost of including some events with likely negligible true market impact.
- **GDELT is treated as weather, not events:** rather than turning ~4,018 days of aggregated global news activity into individual dateable "events" (which would dilute the signal — each day's average already smooths over 87,000–278,000 raw news records), GDELT is kept as a continuous daily background reading merged into the master dataset. This is a deliberate design decision, recorded in the project's decision log, not an oversight.

## What was not found

No fine-tuned sentiment model — FinBERT here is the pretrained `ProsusAI/finbert` model, applied to document *titles* only, not full text, and not retrained on any labelled dataset specific to this project. No claim is made that GDELT's daily reading captures individually dateable "events" — it deliberately does not.

## Limitations

- **Title-only scoring:** FinBERT sees only document titles, not full body text, which likely misses nuance a full-text read would capture.
- **Neutral-class dominance:** with 94.9% of APP sentiment scored neutral, the sentiment signal is sparse — most of the discriminating power in the causal stage comes from event type and the high-impact flag, not sentiment polarity itself.
- **A known upstream data artefact:** two duplicate `(date, title, doc_type)` rows were found and flagged (the same 2017 statement appearing twice in the source archive under two different document-type labels) — this is a source-data quirk, not an error introduced by this notebook.

## How this connects to the next stage

The high-impact event subset and the daily sentiment series built here are the direct inputs to Stage 4's event study and causal analysis — that stage measures whether these categorised, sentiment-scored events actually moved the market, and whether that relationship holds up once genuine confounders (like general market volatility) are accounted for.

## Where to go for more detail

- The notebook itself: `notebooks/03_event_detection.ipynb`
- Feature/column definitions: [`06_feature_dictionary.md`](../research_bible/06_feature_dictionary.md)
- The GDELT-as-continuous-confounder and Sentiment Engine Freeze decisions: [`10_decision_log.md`](../research_bible/10_decision_log.md), entries dated 2026-07-13
