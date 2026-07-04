"""
test_features.py
================
Unit tests for the FeatureEngineer class in src/features.py
"""

import pytest
import numpy as np
import pandas as pd
from src.features import FeatureEngineer


@pytest.fixture
def sample_config():
    return {
        "paths": {"models": "models", "figures": "reports/figures"},
        "model": {"random_seed": 42, "cv_splits": 3},
        "evaluation": {"shap_max_display": 10},
    }


@pytest.fixture
def sample_prices():
    dates = pd.date_range("2022-01-01", periods=300, freq="B")
    np.random.seed(42)
    prices = 100 * np.exp(np.random.normal(0, 0.01, 300).cumsum())
    return pd.DataFrame({"close": prices}, index=dates)


@pytest.fixture
def sample_events():
    dates = pd.date_range("2022-01-01", periods=300, freq="B")
    events = pd.DataFrame({
        "date": dates[[20, 50, 80, 120, 180, 230]],
        "event_type": ["earnings", "macro", "earnings", "geopolitical", "macro", "earnings"],
    })
    return events


def test_add_price_features(sample_config, sample_prices):
    fe = FeatureEngineer(sample_config)
    result = fe.add_price_features(sample_prices)
    assert "return_1d" in result.columns
    assert "vol_21d" in result.columns
    assert "rsi_14d" in result.columns
    assert "momentum_21d" in result.columns


def test_add_event_features(sample_config, sample_prices, sample_events):
    fe = FeatureEngineer(sample_config)
    result = fe.add_price_features(sample_prices)
    result = fe.add_event_features(result, sample_events)
    assert "event_earnings" in result.columns
    assert "event_macro" in result.columns
    assert "total_events_today" in result.columns


def test_build_target(sample_config, sample_prices):
    fe = FeatureEngineer(sample_config)
    target = fe.build_target(sample_prices, forward_days=5)
    assert len(target) == len(sample_prices)
    # Last 5 values should be NaN (no future data)
    assert target.iloc[-1] != target.iloc[-1]  # NaN check


def test_build_pipeline(sample_config, sample_prices, sample_events):
    fe = FeatureEngineer(sample_config)
    X, y = fe.build(sample_prices, sample_events, drop_na=True)
    assert X.shape[0] == y.shape[0]
    assert X.shape[0] > 0
    assert "return_1d" in X.columns
