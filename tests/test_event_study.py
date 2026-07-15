"""
test_event_study.py
====================
Unit tests for the ACTIVE event-study methodology: the constant-mean-return
model implemented inline in `notebooks/04_causal_analysis.ipynb` (cell 6,
`compute_car`) and reproduced, dependency-free, in
`src/event_study_reference.py`.

Replaces the previous `test_event_study.py` (renamed to
`test_legacy_causal_engine.py`), which tested `src/causal_engine.py::EventStudy`
-- a different, unused OLS market-model implementation. See
`docs/research_bible/10_decision_log.md`, 2026-07-15 entry.

These tests use plain Python (no pandas/numpy) so they exercise the reference
implementation exactly as written, and independently recompute expected
values with textbook formulas (mean = sum/n, sample variance = ddof=1) rather
than calling the function under test to derive its own "expected" result.
"""

import math

from src.event_study_reference import (
    ESTIMATION_WINDOW,
    EVENT_WINDOW,
    MIN_ESTIMATION_OBSERVATIONS,
    compute_car_reference,
    find_nearest_trading_day_index,
)


def _independent_mean(values):
    return sum(values) / len(values)


def _independent_sample_stdev(values):
    n = len(values)
    mean = _independent_mean(values)
    return math.sqrt(sum((v - mean) ** 2 for v in values) / (n - 1))


def test_defaults_match_notebook_04():
    """The module's default windows/threshold must match cell 1 of
    notebooks/04_causal_analysis.ipynb exactly -- this is a documentation-
    drift tripwire, not a numerical test."""
    assert ESTIMATION_WINDOW == (-252, -21)
    assert EVENT_WINDOW == (-5, 10)
    assert MIN_ESTIMATION_OBSERVATIONS == 60


def test_car_and_t_stat_against_independent_hand_computation():
    """
    Fully hand-checkable scenario: a 69-day estimation window alternating
    between two known constants (mean/variance computable by anyone with a
    calculator), followed by a 5-day event window of distinct known values.
    Expected CAR/mean_ar/t_stat are computed independently in this test
    (not via the function under test) using textbook formulas.
    """
    returns = [0.0] * 200
    event_idx = 100

    est_window = (-70, -1)  # est_start=30, est_end=99 -> 69 observations
    est_values = [0.01 if i % 2 == 0 else 0.03 for i in range(69)]
    returns[30:99] = est_values

    evt_window = (0, 4)  # evt_start=100, evt_end=105 -> 5 observations
    evt_values = [0.05, -0.02, 0.03, 0.00, 0.01]
    returns[100:105] = evt_values

    expected_mean = _independent_mean(est_values)
    expected_std = _independent_sample_stdev(est_values)
    expected_ar = [v - expected_mean for v in evt_values]
    expected_car = sum(expected_ar)
    expected_mean_ar = expected_car / len(expected_ar)
    expected_t_stat = expected_car / (expected_std * math.sqrt(len(evt_values)))

    result = compute_car_reference(event_idx, returns, est_window=est_window, evt_window=evt_window)

    assert result is not None
    assert result["n_est_days"] == 69
    assert result["n_event_days"] == 5
    assert math.isclose(result["est_expected_return"], expected_mean, rel_tol=1e-12)
    assert math.isclose(result["est_std"], expected_std, rel_tol=1e-12)
    assert math.isclose(result["car"], expected_car, rel_tol=1e-12)
    assert math.isclose(result["mean_ar"], expected_mean_ar, rel_tol=1e-12)
    assert math.isclose(result["t_stat"], expected_t_stat, rel_tol=1e-12)
    assert 0.0 <= result["p_value"] <= 1.0


def test_estimation_window_uses_default_notebook_windows():
    """Sanity check with the real Notebook 04 default windows (-252,-21)/(-5,10)
    and the 60-observation minimum, using a long synthetic series."""
    n = 400
    returns = [0.001 if i % 3 == 0 else -0.0005 for i in range(n)]
    event_idx = 300  # est_start=48, est_end=279 (231 obs); evt 295..310 (16 obs)

    result = compute_car_reference(event_idx, returns)
    assert result is not None
    assert result["n_est_days"] == 231
    assert result["n_event_days"] == 16


def test_insufficient_estimation_history_at_series_start():
    """If the estimation window would start before index 0, return None --
    matches Notebook 04's `if est_start < 0: return None`."""
    returns = [0.001] * 300
    event_idx = 100  # est_start = 100-252 = -152 < 0
    result = compute_car_reference(event_idx, returns)
    assert result is None


def test_insufficient_estimation_history_below_60_observations():
    """Fewer than 60 valid estimation-window observations (after dropping
    missing values) must return None, matching Notebook 04's threshold."""
    returns = [0.0] * 200
    event_idx = 100
    est_window = (-50, -1)  # only 49 raw observations available
    result = compute_car_reference(event_idx, returns, est_window=est_window)
    assert result is None


def test_missing_values_are_dropped_not_zero_filled():
    """NaN values inside the estimation or event window must be excluded from
    the mean/std/CAR computation, not treated as zero -- matches pandas'
    `.dropna()` behaviour in Notebook 04."""
    returns = [0.0] * 200
    event_idx = 100
    est_window = (-70, -1)
    est_values = [0.02] * 69
    # Inject 5 NaNs into the estimation window; 64 valid observations remain (still >= 60)
    for i in range(5):
        est_values[i] = float("nan")
    returns[30:99] = est_values

    result = compute_car_reference(event_idx, returns, est_window=est_window, evt_window=(0, 4))
    assert result is not None
    assert result["n_est_days"] == 64
    # Mean of the remaining 64 valid values (all 0.02) must be exactly 0.02,
    # not skewed toward zero by treating the NaNs as 0.0.
    assert math.isclose(result["est_expected_return"], 0.02, rel_tol=1e-12)


def test_event_window_outside_available_data_returns_none():
    """If the event window would extend past the end of the series, return
    None -- matches `if evt_start < 0 or evt_end > len(spy_sorted): return None`."""
    returns = [0.001] * 120
    event_idx = 115  # evt_end = 115+10+1 = 126 > len(returns)=120
    result = compute_car_reference(event_idx, returns, est_window=(-90, -21))
    assert result is None


def test_event_date_not_on_a_trading_day_maps_to_nearest():
    """find_nearest_trading_day_index must resolve a non-trading-day event
    date (e.g. a weekend) to the nearest actual trading day, matching
    Notebook 04's `diffs.idxmin()` logic."""
    import datetime

    # Explicit trading calendar with a deliberate gap for the weekend of
    # 2020-01-04 (Sat) / 2020-01-05 (Sun): Friday 2020-01-03, then Monday 2020-01-06.
    trading_days = [
        datetime.date(2020, 1, 2),  # Thu
        datetime.date(2020, 1, 3),  # Fri
        datetime.date(2020, 1, 6),  # Mon
        datetime.date(2020, 1, 7),  # Tue
    ]

    saturday = datetime.date(2020, 1, 4)  # not a trading day
    assert saturday not in trading_days

    idx = find_nearest_trading_day_index(trading_days, saturday)
    resolved_date = trading_days[idx]
    # Saturday is 1 day after Friday (01-03) and 2 days before Monday (01-06) ->
    # nearest trading day must be Friday.
    assert resolved_date == datetime.date(2020, 1, 3)

    sunday = datetime.date(2020, 1, 5)  # 2 days after Friday, 1 day before Monday
    idx2 = find_nearest_trading_day_index(trading_days, sunday)
    assert trading_days[idx2] == datetime.date(2020, 1, 6)


def test_deterministic_repeat_calls_are_identical():
    """Calling compute_car_reference twice with identical inputs must return
    byte-identical results -- no hidden global state, no randomness."""
    returns = [0.0005 * ((i % 13) - 6) for i in range(400)]
    event_idx = 300

    result_1 = compute_car_reference(event_idx, returns)
    result_2 = compute_car_reference(event_idx, returns)
    assert result_1 == result_2


def test_no_look_ahead_leakage_in_estimation_window():
    """Perturbing returns strictly AFTER the estimation window's end index
    (est_end = event_idx + est_window[1]) must not change the computed
    est_expected_return/est_std/n_est_days -- proves the estimation baseline
    never reads future-relative-to-itself data. Also perturbs event-window
    and post-event-window values to confirm they don't leak backward into
    the estimation statistics either."""
    n = 400
    base_returns = [0.001 if i % 5 == 0 else -0.0002 for i in range(n)]
    event_idx = 300
    est_end_index = event_idx + ESTIMATION_WINDOW[1]  # = 279, exclusive end

    result_baseline = compute_car_reference(event_idx, base_returns)
    assert result_baseline is not None

    perturbed_returns = list(base_returns)
    # Perturb every return from est_end_index onward (event window and beyond)
    for i in range(est_end_index, n):
        perturbed_returns[i] = 999.0  # deliberately extreme, would be obvious if leaked

    result_perturbed = compute_car_reference(event_idx, perturbed_returns)
    # Estimation-window statistics must be completely unaffected
    assert result_perturbed is not None
    assert result_perturbed["est_expected_return"] == result_baseline["est_expected_return"]
    assert result_perturbed["est_std"] == result_baseline["est_std"]
    assert result_perturbed["n_est_days"] == result_baseline["n_est_days"]
    # (car/t_stat/p_value legitimately change, since the event window itself was perturbed --
    #  that is expected and correct, not a leakage failure.)
