"""
causal_engine.py
================
Causal inference methods for quantifying event-driven market impact.
  - Classical Event Study (abnormal returns, CAR)
  - DoWhy causal graph estimation
  - Difference-in-Differences (DiD)

Usage:
    from src.causal_engine import EventStudy, CausalImpactEstimator
"""

import logging
import numpy as np
import pandas as pd
from typing import Optional, List, Tuple
from scipy import stats

logger = logging.getLogger(__name__)


class EventStudy:
    """
    Classical event study methodology (Fama, Fisher, Jensen & Roll, 1969).

    Measures abnormal returns (AR) and cumulative abnormal returns (CAR)
    around event dates, using a market model as the benchmark.

    Can be instantiated directly or via EventStudy.from_config(config).

    Parameters
    ----------
    estimation_window : int
        Number of trading days before the event window used to estimate
        expected returns (default: 120)
    pre_window : int
        Days before event to include in event window (default: 5)
    post_window : int
        Days after event to include in event window (default: 10)
    """

    def __init__(
        self,
        estimation_window: int = 120,
        pre_window: int = 5,
        post_window: int = 10,
    ):
        self.estimation_window = estimation_window
        self.pre_window = pre_window
        self.post_window = post_window

    @classmethod
    def from_config(cls, config: dict) -> "EventStudy":
        """
        Instantiate from project config.yaml (reads config['data'] section).

        Usage:
            es = EventStudy.from_config(config)
        """
        data_cfg = config.get("data", {})
        return cls(
            estimation_window=data_cfg.get("estimation_window", 120),
            pre_window=data_cfg.get("event_window_pre", 5),
            post_window=data_cfg.get("event_window_post", 10),
        )

    def compute_returns(self, prices: pd.Series) -> pd.Series:
        """Compute log returns from price series."""
        return np.log(prices / prices.shift(1)).dropna()

    def estimate_market_model(
        self,
        asset_returns: pd.Series,
        market_returns: pd.Series,
        estimation_dates: pd.DatetimeIndex,
    ) -> Tuple[float, float]:
        """
        OLS regression of asset returns on market returns over estimation window.

        Returns
        -------
        (alpha, beta) : Tuple[float, float]
        """
        asset_est = asset_returns.loc[estimation_dates]
        market_est = market_returns.loc[estimation_dates]

        # Align
        aligned = pd.concat([asset_est, market_est], axis=1).dropna()
        if len(aligned) < 30:
            logger.warning("Estimation window too short for reliable OLS")

        slope, intercept, r, p, se = stats.linregress(
            aligned.iloc[:, 1].values, aligned.iloc[:, 0].values
        )
        return intercept, slope  # alpha, beta

    def compute_car(
        self,
        asset_returns: pd.Series,
        market_returns: pd.Series,
        event_date: pd.Timestamp,
    ) -> pd.DataFrame:
        """
        Compute Abnormal Returns (AR) and Cumulative AR (CAR) for one event.

        Parameters
        ----------
        asset_returns : pd.Series
            Daily log returns of the asset
        market_returns : pd.Series
            Daily log returns of the market benchmark
        event_date : pd.Timestamp
            The event date (day 0)

        Returns
        -------
        pd.DataFrame
            DataFrame with columns: date, t, AR, CAR, t_stat
        """
        all_dates = asset_returns.index.sort_values()
        if event_date not in all_dates:
            logger.warning(f"Event date {event_date} not in returns index")
            return pd.DataFrame()

        event_idx = all_dates.get_loc(event_date)

        # Estimation window
        est_start = max(0, event_idx - self.pre_window - self.estimation_window)
        est_end = event_idx - self.pre_window
        estimation_dates = all_dates[est_start:est_end]

        if len(estimation_dates) < 30:
            logger.warning("Insufficient estimation window data")
            return pd.DataFrame()

        alpha, beta = self.estimate_market_model(
            asset_returns, market_returns, estimation_dates
        )

        # Event window
        ev_start = max(0, event_idx - self.pre_window)
        ev_end = min(len(all_dates), event_idx + self.post_window + 1)
        event_dates = all_dates[ev_start:ev_end]

        records = []
        car = 0.0
        for t, date in enumerate(event_dates):
            t_rel = t - self.pre_window  # t=0 is event day
            if date not in asset_returns.index or date not in market_returns.index:
                continue
            actual = asset_returns.loc[date]
            expected = alpha + beta * market_returns.loc[date]
            ar = actual - expected
            car += ar
            records.append({
                "date": date,
                "t": t_rel,
                "actual_return": actual,
                "expected_return": expected,
                "AR": ar,
                "CAR": car,
            })

        result = pd.DataFrame(records)

        # Compute t-statistic using estimation window residuals
        est_actual = asset_returns.loc[estimation_dates]
        est_market = market_returns.loc[estimation_dates]
        est_expected = alpha + beta * est_market
        residuals = est_actual - est_expected
        sigma = residuals.std()

        if sigma > 0:
            result["t_stat"] = result["AR"] / sigma
        else:
            result["t_stat"] = np.nan

        return result

    def run_event_study(
        self,
        asset_returns: pd.Series,
        market_returns: pd.Series,
        event_dates: List[pd.Timestamp],
    ) -> pd.DataFrame:
        """
        Run event study across multiple event dates and aggregate results.

        Returns
        -------
        pd.DataFrame
            Average AR and CAR by relative event day (t), with significance.
        """
        all_results = []
        for event_date in event_dates:
            result = self.compute_car(asset_returns, market_returns, event_date)
            if not result.empty:
                result["event_date"] = event_date
                all_results.append(result)

        if not all_results:
            logger.error("No valid event results computed")
            return pd.DataFrame()

        combined = pd.concat(all_results, ignore_index=True)

        # Average by relative day
        avg = (
            combined.groupby("t")
            .agg(
                mean_AR=("AR", "mean"),
                mean_CAR=("CAR", "mean"),
                std_AR=("AR", "std"),
                n_events=("AR", "count"),
            )
            .reset_index()
        )
        avg["se_AR"] = avg["std_AR"] / np.sqrt(avg["n_events"])
        avg["t_stat"] = avg["mean_AR"] / avg["se_AR"]
        avg["p_value"] = 2 * (1 - stats.t.cdf(np.abs(avg["t_stat"]), df=avg["n_events"] - 1))
        avg["significant_05"] = avg["p_value"] < 0.05

        return avg


class CausalImpactEstimator:
    """
    Wraps Microsoft's DoWhy library for causal effect estimation.

    Uses a structural causal model where:
      Treatment = event occurrence (binary)
      Outcome = asset return in event window
      Confounders = market return, VIX, sector momentum

    Parameters
    ----------
    method : str
        DoWhy estimation method name
    """

    def __init__(self, method: str = "backdoor.linear_regression"):
        self.method = method

    @classmethod
    def from_config(cls, config: dict) -> "CausalImpactEstimator":
        """
        Instantiate from project config.yaml (reads config['causal'] section).

        Usage:
            estimator = CausalImpactEstimator.from_config(config)
        """
        causal_cfg = config.get("causal", {})
        return cls(method=causal_cfg.get("method", "backdoor.linear_regression"))

    def estimate(
        self,
        data: pd.DataFrame,
        treatment_col: str,
        outcome_col: str,
        confounder_cols: List[str],
    ) -> dict:
        """
        Estimate the Average Treatment Effect (ATE) of an event on returns.

        Parameters
        ----------
        data : pd.DataFrame
            Panel data with treatment, outcome, and confounder columns
        treatment_col : str
            Binary column: 1 = event occurred, 0 = no event
        outcome_col : str
            Continuous column: asset return
        confounder_cols : list[str]
            Columns to control for as confounders

        Returns
        -------
        dict with keys: ate, confidence_interval, p_value, refutation_results
        """
        try:
            import dowhy
            from dowhy import CausalModel
        except ImportError:
            raise ImportError("Install dowhy: pip install dowhy")

        # Build causal graph (DAG in DOT notation)
        confounders_dot = " -> ".join([f'"{c}" -> "{outcome_col}"' for c in confounder_cols])
        treatment_confounder_dot = " ".join(
            [f'"{c}" -> "{treatment_col}";' for c in confounder_cols]
        )
        graph_dot = (
            f'digraph {{'
            f'"{treatment_col}" -> "{outcome_col}"; '
            f'{treatment_confounder_dot}'
            f'}}'
        )

        model = CausalModel(
            data=data,
            treatment=treatment_col,
            outcome=outcome_col,
            graph=graph_dot,
        )

        identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
        estimate = model.estimate_effect(
            identified_estimand,
            method_name=self.method,
        )

        # Refutation tests
        refutation_results = {}
        for refuter_name in ["random_common_cause", "placebo_treatment_refuter"]:
            try:
                refutation = model.refute_estimate(
                    identified_estimand,
                    estimate,
                    method_name=refuter_name,
                )
                refutation_results[refuter_name] = {
                    "estimated_effect": refutation.estimated_effect,
                    "new_effect": refutation.new_effect,
                    "p_value": getattr(refutation, "refutation_result", {}).get("p_value", None),
                }
            except Exception as e:
                logger.warning(f"Refutation test {refuter_name} failed: {e}")

        return {
            "ate": estimate.value,
            "estimand": str(identified_estimand),
            "refutation_results": refutation_results,
        }
