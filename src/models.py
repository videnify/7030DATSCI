"""
models.py
=========
Model training, tuning and persistence.
  - Baseline: LASSO regression
  - Primary: XGBoost / LightGBM
  - Time-series cross-validation (no leakage)

Usage:
    from src.models import ModelTrainer
    trainer = ModelTrainer(config)
    results = trainer.train_all(X_train, y_train)
"""

import logging
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Tuple

from sklearn.linear_model import LassoCV, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)


def directional_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Fraction of predictions with the correct sign (direction)."""
    return np.mean(np.sign(y_true) == np.sign(y_pred))


class ModelTrainer:
    """
    Trains and evaluates predictive models for market impact forecasting.

    All models use TimeSeriesSplit CV to prevent data leakage.

    Parameters
    ----------
    config : dict
        Project config (random_seed, cv_splits, model hyperparameters)
    """

    def __init__(self, config: dict):
        self.config = config
        self.seed = config["model"]["random_seed"]
        self.n_splits = config["model"]["cv_splits"]
        self.models_path = Path(config["paths"]["models"])
        self.models_path.mkdir(parents=True, exist_ok=True)
        self.trained_models: Dict = {}
        self.cv = TimeSeriesSplit(n_splits=self.n_splits)

    def _lasso_baseline(self) -> Pipeline:
        """LASSO regression with cross-validated alpha selection."""
        return Pipeline([
            ("scaler", StandardScaler()),
            ("model", LassoCV(cv=5, random_state=self.seed, max_iter=5000)),
        ])

    def _xgboost_model(self) -> object:
        """XGBoost regressor with configured hyperparameters."""
        try:
            from xgboost import XGBRegressor
        except ImportError:
            raise ImportError("Install xgboost: pip install xgboost")

        cfg = self.config["model"]["xgboost"]
        return XGBRegressor(
            n_estimators=cfg["n_estimators"],
            learning_rate=cfg["learning_rate"],
            max_depth=cfg["max_depth"],
            subsample=cfg["subsample"],
            colsample_bytree=cfg["colsample_bytree"],
            early_stopping_rounds=cfg.get("early_stopping_rounds", 50),
            random_state=self.seed,
            n_jobs=-1,
            verbosity=0,
        )

    def _lightgbm_model(self) -> object:
        """LightGBM regressor with configured hyperparameters."""
        try:
            from lightgbm import LGBMRegressor
        except ImportError:
            raise ImportError("Install lightgbm: pip install lightgbm")

        cfg = self.config["model"]["lightgbm"]
        return LGBMRegressor(
            n_estimators=cfg["n_estimators"],
            learning_rate=cfg["learning_rate"],
            num_leaves=cfg["num_leaves"],
            subsample=cfg["subsample"],
            random_state=self.seed,
            n_jobs=-1,
            verbose=-1,
        )

    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """Compute standard regression metrics + directional accuracy."""
        return {
            "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
            "mae": mean_absolute_error(y_true, y_pred),
            "r2": r2_score(y_true, y_pred),
            "directional_accuracy": directional_accuracy(y_true, y_pred),
        }

    def train_all(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        X_test: Optional[pd.DataFrame] = None,
        y_test: Optional[pd.Series] = None,
    ) -> Dict:
        """
        Train LASSO, XGBoost, and LightGBM models; evaluate via TimeSeriesSplit CV.

        Parameters
        ----------
        X : pd.DataFrame, y : pd.Series
            Training features and target
        X_test, y_test : optional
            Held-out test set for final evaluation

        Returns
        -------
        dict
            { model_name: { "cv_scores": [...], "test_scores": {...}, "model": obj } }
        """
        X_arr = X.values if isinstance(X, pd.DataFrame) else X
        y_arr = y.values if isinstance(y, pd.Series) else y

        model_registry = {
            "lasso": self._lasso_baseline(),
            "xgboost": self._xgboost_model(),
            "lightgbm": self._lightgbm_model(),
        }

        results = {}

        for name, model in model_registry.items():
            logger.info(f"Training {name}...")

            # TimeSeriesSplit CV
            cv_rmse = []
            cv_da = []
            for fold, (train_idx, val_idx) in enumerate(self.cv.split(X_arr)):
                X_tr, X_val = X_arr[train_idx], X_arr[val_idx]
                y_tr, y_val = y_arr[train_idx], y_arr[val_idx]
                model.fit(X_tr, y_tr)
                preds = model.predict(X_val)
                metrics = self.evaluate(y_val, preds)
                cv_rmse.append(metrics["rmse"])
                cv_da.append(metrics["directional_accuracy"])
                logger.info(
                    f"  Fold {fold+1}: RMSE={metrics['rmse']:.4f}, DA={metrics['directional_accuracy']:.3f}"
                )

            # Refit on full training set
            model.fit(X_arr, y_arr)

            test_scores = {}
            if X_test is not None and y_test is not None:
                test_preds = model.predict(X_test.values if isinstance(X_test, pd.DataFrame) else X_test)
                test_scores = self.evaluate(y_test.values if isinstance(y_test, pd.Series) else y_test, test_preds)
                logger.info(f"  Test RMSE={test_scores['rmse']:.4f}, DA={test_scores['directional_accuracy']:.3f}")

            self.trained_models[name] = model
            results[name] = {
                "cv_rmse_mean": np.mean(cv_rmse),
                "cv_rmse_std": np.std(cv_rmse),
                "cv_da_mean": np.mean(cv_da),
                "cv_scores": {"rmse": cv_rmse, "directional_accuracy": cv_da},
                "test_scores": test_scores,
                "model": model,
            }

            self.save_model(name, model)

        return results

    def save_model(self, name: str, model) -> Path:
        """Persist a trained model to disk."""
        path = self.models_path / f"{name}.joblib"
        joblib.dump(model, path)
        logger.info(f"Saved {name} → {path}")
        return path

    def load_model(self, name: str):
        """Load a saved model from disk."""
        path = self.models_path / f"{name}.joblib"
        if not path.exists():
            raise FileNotFoundError(f"No saved model at {path}")
        return joblib.load(path)
