"""
features.py
===========
Feature engineering pipeline for the predictive model layer.
Builds a feature matrix from price data, event data, and sentiment scores.

Usage:
    from src.features import FeatureEngineer
    fe = FeatureEngineer(config)
    X, y = fe.build(prices_df, events_df)
"""

import logging
import numpy as np
import pandas as pd
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """
    Constructs the model feature matrix from multi-source data.

    Features generated:
      Price-based: lagged returns, rolling volatility, momentum, RSI, ATR
      Event-based: event_type dummies, days_since_event, event_count_window
      Sentiment: lagged sentiment scores per event type
      Macro: VIX, yield curve slope (if available)

    Parameters
    ----------
    config : dict
        Project config (for window sizes and feature toggles)
    """

    def __init__(self, config: dict):
        self.config = config

    def add_price_features(self, df: pd.DataFrame, price_col: str = "close") -> pd.DataFrame:
        """Add technical / price-derived features."""
        df = df.copy()
        p = df[price_col]

        # Log returns
        df["return_1d"] = np.log(p / p.shift(1))
        df["return_2d"] = np.log(p / p.shift(2))
        df["return_5d"] = np.log(p / p.shift(5))
        df["return_10d"] = np.log(p / p.shift(10))
        df["return_21d"] = np.log(p / p.shift(21))

        # Rolling volatility (realised vol)
        df["vol_5d"] = df["return_1d"].rolling(5).std() * np.sqrt(252)
        df["vol_21d"] = df["return_1d"].rolling(21).std() * np.sqrt(252)
        df["vol_63d"] = df["return_1d"].rolling(63).std() * np.sqrt(252)

        # Momentum
        df["momentum_21d"] = p / p.shift(21) - 1
        df["momentum_63d"] = p / p.shift(63) - 1

        # RSI (14-day)
        delta = p.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / (loss + 1e-9)
        df["rsi_14d"] = 100 - 100 / (1 + rs)

        # Bollinger band width (normalised)
        bb_mid = p.rolling(20).mean()
        bb_std = p.rolling(20).std()
        df["bb_width"] = (2 * bb_std) / (bb_mid + 1e-9)

        # Lagged returns as features
        for lag in [1, 2, 3, 5, 10]:
            df[f"lag_return_{lag}d"] = df["return_1d"].shift(lag)

        return df

    def add_event_features(
        self, df: pd.DataFrame, events_df: pd.DataFrame, lookback_days: int = 10
    ) -> pd.DataFrame:
        """
        Add event-based features:
          - Whether an event occurred on each day (by type)
          - Number of events in the last N days
          - Days since last event of each type

        Parameters
        ----------
        df : pd.DataFrame
            Main DataFrame with DatetimeIndex
        events_df : pd.DataFrame
            Event DataFrame with 'date' and 'event_type' columns
        lookback_days : int
            Rolling window for event count features
        """
        df = df.copy()
        events_df = events_df.copy()
        events_df["date"] = pd.to_datetime(events_df["date"])
        all_dates = df.index

        event_types = events_df["event_type"].unique()

        for etype in event_types:
            etype_events = events_df[events_df["event_type"] == etype]["date"]

            # Binary: did this event type occur today?
            df[f"event_{etype}"] = df.index.isin(etype_events).astype(int)

            # Rolling count of events in last N days
            event_series = df[f"event_{etype}"]
            df[f"event_{etype}_count_{lookback_days}d"] = (
                event_series.rolling(lookback_days, min_periods=1).sum()
            )

            # Days since last event of this type
            df[f"days_since_{etype}"] = np.nan
            last_event = None
            for date in all_dates:
                if date in etype_events.values:
                    last_event = date
                if last_event is not None:
                    df.loc[date, f"days_since_{etype}"] = (date - last_event).days

        # Total event count across all types
        event_cols = [f"event_{etype}" for etype in event_types]
        df["total_events_today"] = df[event_cols].sum(axis=1)

        return df

    def add_sentiment_features(
        self, df: pd.DataFrame, sentiment_df: pd.DataFrame, lags: List[int] = [0, 1, 2, 3]
    ) -> pd.DataFrame:
        """
        Join daily aggregated sentiment scores and add lagged versions.

        Parameters
        ----------
        df : pd.DataFrame
            Main DataFrame with DatetimeIndex
        sentiment_df : pd.DataFrame
            Output of EventDetector.aggregate_daily_sentiment()
        lags : list[int]
            Lag days for sentiment features
        """
        df = df.copy()
        sentiment_df = sentiment_df.copy()
        sentiment_df["date"] = pd.to_datetime(sentiment_df["date"])

        # Pivot to wide format: one column per event_type
        pivot = sentiment_df.pivot_table(
            index="date",
            columns="event_type",
            values=["mean_sentiment", "article_count"],
            aggfunc="mean",
        )
        pivot.columns = [f"{col[0]}_{col[1]}" for col in pivot.columns]
        pivot = pivot.reindex(df.index, method="ffill")

        for col in pivot.columns:
            df[col] = pivot[col]
            for lag in lags:
                if lag > 0:
                    df[f"{col}_lag{lag}"] = pivot[col].shift(lag)

        return df

    def build_target(
        self, df: pd.DataFrame, forward_days: int = 5, price_col: str = "close"
    ) -> pd.Series:
        """
        Build the prediction target: forward N-day return.

        Parameters
        ----------
        forward_days : int
            How many days ahead to predict
        """
        forward_return = np.log(
            df[price_col].shift(-forward_days) / df[price_col]
        )
        return forward_return

    def build(
        self,
        prices_df: pd.DataFrame,
        events_df: pd.DataFrame,
        sentiment_df: Optional[pd.DataFrame] = None,
        target_forward_days: int = 5,
        price_col: str = "close",
        drop_na: bool = True,
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Full pipeline: build feature matrix X and target y.

        Parameters
        ----------
        prices_df : pd.DataFrame
            OHLCV price data (DatetimeIndex)
        events_df : pd.DataFrame
            Event data with 'date' and 'event_type' columns
        sentiment_df : pd.DataFrame, optional
            Daily sentiment scores from EventDetector
        target_forward_days : int
            Forecast horizon for target variable

        Returns
        -------
        X : pd.DataFrame, y : pd.Series
        """
        df = prices_df.copy()
        df = self.add_price_features(df, price_col=price_col)
        df = self.add_event_features(df, events_df)

        if sentiment_df is not None:
            df = self.add_sentiment_features(df, sentiment_df)

        y = self.build_target(df, forward_days=target_forward_days, price_col=price_col)
        df["target"] = y

        if drop_na:
            df = df.dropna()

        y = df.pop("target")
        X = df.drop(columns=[price_col], errors="ignore")

        logger.info(f"Feature matrix: {X.shape[0]} rows × {X.shape[1]} features")
        return X, y
