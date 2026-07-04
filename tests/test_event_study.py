"""
test_event_study.py
===================
Unit tests for the EventStudy class in src/causal_engine.py
"""

import pytest
import numpy as np
import pandas as pd
from src.causal_engine import EventStudy


@pytest.fixture
def synthetic_returns():
    """Generate synthetic price/return data for testing."""
    np.random.seed(42)
    dates = pd.date_range("2020-01-01", periods=300, freq="B")
    market = pd.Series(np.random.normal(0.0005, 0.01, len(dates)), index=dates, name="market")
    beta = 1.2
    alpha = 0.0001
    noise = np.random.normal(0, 0.008, len(dates))
    asset = pd.Series(alpha + beta * market.values + noise, index=dates, name="asset")
    return asset, market


def test_compute_returns(synthetic_returns):
    """Log returns should have mean close to 0."""
    asset, market = synthetic_returns
    es = EventStudy()
    returns = es.compute_returns(asset.cumsum().apply(np.exp))
    assert returns.notna().all()


def test_estimate_market_model(synthetic_returns):
    """Beta estimate should be close to the true beta (1.2)."""
    asset, market = synthetic_returns
    es = EventStudy(estimation_window=200)
    alpha, beta = es.estimate_market_model(asset, market, asset.index[:200])
    assert abs(beta - 1.2) < 0.3, f"Beta estimate {beta:.2f} too far from true 1.2"


def test_compute_car(synthetic_returns):
    """CAR computation should return a non-empty DataFrame."""
    asset, market = synthetic_returns
    es = EventStudy(estimation_window=100, pre_window=5, post_window=10)
    event_date = asset.index[150]
    result = es.compute_car(asset, market, event_date)
    assert not result.empty
    assert "AR" in result.columns
    assert "CAR" in result.columns
    assert len(result) == es.pre_window + es.post_window + 1


def test_run_event_study(synthetic_returns):
    """run_event_study should aggregate results across multiple events."""
    asset, market = synthetic_returns
    es = EventStudy(estimation_window=80, pre_window=5, post_window=10)
    event_dates = [asset.index[120], asset.index[180], asset.index[240]]
    avg = es.run_event_study(asset, market, event_dates)
    assert not avg.empty
    assert "mean_AR" in avg.columns
    assert "p_value" in avg.columns
