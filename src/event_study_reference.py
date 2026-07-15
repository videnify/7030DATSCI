"""
event_study_reference.py
=========================
Pure, dependency-free reference implementation of the constant-mean-return
event-study methodology actually used in `notebooks/04_causal_analysis.ipynb`
(cell 6, `compute_car`). Deliberately independent of pandas/numpy so it can
be unit-tested in isolation from the notebook's runtime.

This module exists to close a coverage gap: the only prior event-study unit
test (`tests/test_event_study.py`) tested `src/causal_engine.py::EventStudy`,
an OLS market-model regression class that is not used anywhere in the current
pipeline (see `docs/research_bible/03_methodology.md`). Notebook 04's actual
method is a simple constant-mean-return model (expected return = the mean of
the estimation-window returns, not a regression), with different default
windows. See `docs/research_bible/10_decision_log.md`, 2026-07-15 entry.

This is a regression-test reference only. Notebook 04 has not been refactored
to import it -- see the same decision-log entry for why.
"""

import math
from typing import List, Optional, Sequence, Tuple


ESTIMATION_WINDOW = (-252, -21)  # matches notebooks/04_causal_analysis.ipynb cell 1
EVENT_WINDOW = (-5, 10)          # matches notebooks/04_causal_analysis.ipynb cell 1
MIN_ESTIMATION_OBSERVATIONS = 60  # matches the `if len(est_returns) < 60` check in cell 6


def _sample_stdev(values: Sequence[float]) -> float:
    """Sample standard deviation (ddof=1), matching pandas' `.std()` default
    used by Notebook 04's `est_returns.std()` call."""
    n = len(values)
    if n < 2:
        return float("nan")
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / (n - 1)
    return math.sqrt(variance)


def find_nearest_trading_day_index(dates: Sequence, event_date) -> int:
    """
    Map an arbitrary event date (which may fall on a non-trading day, e.g. a
    weekend) to the index of the nearest trading day in `dates`.

    Mirrors Notebook 04 cell 6 exactly:
        diffs = (spy_sorted['date'] - event_date).abs()
        idx = int(diffs.idxmin())

    `dates` must be sorted ascending. Ties (equidistant on both sides) resolve
    to the earlier index, matching pandas' `.idxmin()` (first minimum wins).
    """
    best_idx = 0
    best_diff = None
    for i, d in enumerate(dates):
        diff = abs((d - event_date).days) if hasattr(d - event_date, "days") else abs(d - event_date)
        if best_diff is None or diff < best_diff:
            best_diff = diff
            best_idx = i
    return best_idx


def compute_car_reference(
    event_idx: int,
    returns: Sequence[Optional[float]],
    est_window: Tuple[int, int] = ESTIMATION_WINDOW,
    evt_window: Tuple[int, int] = EVENT_WINDOW,
) -> Optional[dict]:
    """
    Reference implementation of Notebook 04's `compute_car`, operating on a
    plain sequence of daily returns indexed by integer trading-day position
    instead of a pandas DataFrame indexed by calendar date.

    Parameters
    ----------
    event_idx : int
        Integer position of the event's (already-resolved) nearest trading
        day within `returns`.
    returns : Sequence[Optional[float]]
        Daily returns for the full trading calendar, in chronological order.
        `None` or `NaN` entries are treated as missing (dropped), matching
        pandas' `.dropna()`.
    est_window : tuple[int, int]
        (start_offset, end_offset) relative to `event_idx`, end exclusive.
        Default (-252, -21) matches Notebook 04.
    evt_window : tuple[int, int]
        (start_offset, end_offset_inclusive) relative to `event_idx`.
        Default (-5, 10) matches Notebook 04 (both endpoints included).

    Returns
    -------
    dict or None
        None if there is insufficient estimation history (start index < 0,
        or fewer than 60 non-missing estimation-window observations), or if
        the event window falls outside the available data range -- mirrors
        Notebook 04's `compute_car` return-None conditions exactly.

        On success, a dict with keys: car, mean_ar, n_event_days, n_est_days,
        est_expected_return, est_std, t_stat, p_value, significant.
    """
    n_total = len(returns)

    est_start = event_idx + est_window[0]
    est_end = event_idx + est_window[1]
    if est_start < 0:
        return None

    est_returns = [r for r in returns[max(est_start, 0):est_end] if r is not None and not _is_nan(r)]
    if len(est_returns) < MIN_ESTIMATION_OBSERVATIONS:
        return None

    expected_return = sum(est_returns) / len(est_returns)
    est_std = _sample_stdev(est_returns)

    evt_start = event_idx + evt_window[0]
    evt_end = event_idx + evt_window[1] + 1  # +1: Notebook 04 treats evt_window[1] as inclusive
    if evt_start < 0 or evt_end > n_total:
        return None

    evt_returns = [r for r in returns[evt_start:evt_end] if r is not None and not _is_nan(r)]
    ar = [r - expected_return for r in evt_returns]
    # CAR is the cumulative sum's final value, i.e. the plain sum of ar.
    car = sum(ar) if len(ar) > 0 else float("nan")

    n = len(ar)
    if est_std > 0 and n > 0:
        t_stat = car / (est_std * math.sqrt(n))
    else:
        t_stat = float("nan")

    if not _is_nan(t_stat):
        p_value = 2 * (1 - _student_t_cdf(abs(t_stat), df=n - 1))
    else:
        p_value = float("nan")

    return {
        "car": car,
        "mean_ar": (sum(ar) / len(ar)) if len(ar) > 0 else float("nan"),
        "n_event_days": n,
        "n_est_days": len(est_returns),
        "est_expected_return": expected_return,
        "est_std": est_std,
        "t_stat": t_stat,
        "p_value": p_value,
        "significant": bool(p_value < 0.05) if not _is_nan(p_value) else False,
    }


def _is_nan(x: float) -> bool:
    try:
        return math.isnan(x)
    except TypeError:
        return False


def _student_t_cdf(t: float, df: int) -> float:
    """
    CDF of the Student's t-distribution, dependency-free (no scipy).
    Uses the standard regularized incomplete beta function relationship:
        CDF(t) = 1 - 0.5 * I_x(df/2, 1/2),  x = df / (df + t^2),  for t >= 0
    Accurate to float64 precision for the df/t ranges this module needs
    (df ~ 1-16, |t| < 20). Cross-checked against scipy.stats.t.cdf values
    already printed in Notebook 04's saved output (see test suite).
    """
    if df <= 0:
        return float("nan")
    x = df / (df + t * t)
    ib = _regularized_incomplete_beta(x, df / 2.0, 0.5)
    cdf_of_abs_t_upper_tail = 0.5 * ib  # P(T > |t|) for a two-sided-symmetric t
    return 1.0 - cdf_of_abs_t_upper_tail if t >= 0 else cdf_of_abs_t_upper_tail


def _regularized_incomplete_beta(x: float, a: float, b: float) -> float:
    """Regularized incomplete beta function I_x(a, b) via a continued fraction
    (Numerical Recipes' `betacf`), dependency-free."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    ln_beta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(ln_beta + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(x, a, b) / a
    else:
        return 1.0 - front * _betacf(1.0 - x, b, a) / b


def _betacf(x: float, a: float, b: float, max_iter: int = 200, eps: float = 1e-12) -> float:
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h
