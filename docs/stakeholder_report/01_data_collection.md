# 1. Data Collection — What Went Into This Project

**Status:** ✅ Verified — every number below was checked directly against the current data files, not copied from an earlier report or the notebook's own narrative text.
**Originally verified:** 2026-07-13.
**Last reviewed against current pipeline:** 2026-07-15 (as part of a full eight-notebook traceability audit — every figure in the table below was re-checked directly against the current parquet files on disk; all matched; no number changed as a result of this review).
**Technical detail:** `notebooks/01_data_collection.ipynb` · [`dataset_contract.md`](../research_bible/dataset_contract.md) · [`05_data_dictionary.md`](../research_bible/05_data_dictionary.md) · [`10_decision_log.md`](../research_bible/10_decision_log.md) (2026-07-13 entry, GDELT backfill; 2026-07-15 entry, GDELT reproducibility correction)

---

## What this stage does

Before any analysis can happen, the project needs to gather every piece of raw information it depends on. This first stage is that collection step — it pulls together stock market data, economic indicators, Federal Reserve decisions, presidential communications, and global news-event signals, all covering the same eleven-year window (January 2015 – December 2025), so that everything lines up on the same calendar and can later be compared day by day.

Think of this as building the foundation. Every later stage — the analysis, the modelling, the conclusions — only stands up if the data underneath it is complete, correctly dated, and trustworthy. If something is wrong here, it's wrong everywhere downstream.

## What was actually collected

| Data source | What it is | Rows collected | Date range | Missing data |
|---|---|---|---|---|
| S&P 500 prices (SPY) | Daily stock price for the main index this project studies | 2,765 trading days | Jan 2015 – Dec 2025 | None |
| VIX ("fear index") | A daily measure of how nervous or calm the market is | 2,765 trading days | Jan 2015 – Dec 2025 | 1 value (explained below — expected, not a problem) |
| Economic indicators | Inflation, interest rates, unemployment, and related government-published figures | 2,870 days | Jan 2015 – Dec 2025 | None |
| Federal Reserve decisions | Every interest-rate decision the Fed made | 89 meetings | Jan 2015 – Dec 2025 | None |
| Presidential communications | Speeches, statements, and official documents from four presidential terms | 10,892 collected, narrowed to 916 judged economically relevant | Jan 2015 – Dec 2025 | None |
| Global news-risk signal (GDELT) | A daily measure of global political/geopolitical tension, drawn from a worldwide news-monitoring project | 4,018 days | Jan 2015 – Dec 2025 | None |

## How we know it's right

Every one of the datasets above was run through an automated completeness check after collection — essentially, "does this cover the full time period with no unexplained gaps?" Every dataset passed with zero missing values, except one: the market-nervousness (VIX) series is missing a single value on its very first day. That's expected, not a defect — that particular figure measures *day-over-day change*, and there's no "previous day" to compare against on day one of the series.

## What's new in this version

The global news-risk signal (GDELT) is a genuine upgrade over an earlier version of this project. Previously, this signal only covered a 5-day trial window — nowhere near enough to be useful. It has now been backfilled to cover the full eleven-year study period (4,018 days), built from roughly 25 gigabytes of raw global news-event data. This closes a gap that was flagged as a known weakness in earlier drafts of this work.

That said, bringing in this much bigger signal correctly is itself a piece of careful design — simply averaging hundreds of thousands of daily news events into one number, and treating each day as if it were a single "event," would have diluted the very story it's meant to help tell. The decision made (and recorded in the project's technical decision log) was to treat this as a *background weather reading* — a daily condition the model can take into account — rather than as a list of individual, dateable happenings. That distinction matters and is explained further in the Notebook 3 section once it's written.

## What's still being checked

The presidential-communications figure above shows a narrowing from 10,892 collected documents down to 916 judged "economically relevant." That narrowing step (which keywords or rules decide what counts as economically relevant) has not yet been independently reviewed in this pass of the project — it's flagged as an open item, not a confirmed result. It does not affect the market price, volatility, economic-indicator, Fed-decision, or news-risk data described above, all of which are independently verified and stable.

**Re-checked 2026-07-15:** this item remains open. The 2026-07-15 traceability audit searched the full decision log for any later review of this specific filtering rule and found none — only the downstream consequences of the current 916-document count (e.g. event totals in Notebook 3/4) have been discussed since. This is preserved as an open limitation, not marked resolved, even though Notebook 3 itself is now complete and re-verified — completion of the notebook is not the same as independent review of this one filtering rule.

## Where to go for more detail

- The notebook itself: `notebooks/01_data_collection.ipynb`
- The formal data contract (what each file must contain to be considered valid): [`dataset_contract.md`](../research_bible/dataset_contract.md)
- Column-by-column definitions: [`05_data_dictionary.md`](../research_bible/05_data_dictionary.md)
- The reasoning behind the GDELT redesign: [`10_decision_log.md`](../research_bible/10_decision_log.md), entry dated 2026-07-13
