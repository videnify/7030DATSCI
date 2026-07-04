"""
evaluation.py
=============
Model evaluation, SHAP explainability, and publication-quality visualisation.

Usage:
    from src.evaluation import ModelEvaluator
    evaluator = ModelEvaluator(config)
    evaluator.shap_summary(model, X, feature_names)
    evaluator.plot_car(car_df)
"""

import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from pathlib import Path
from typing import List, Optional, Dict

logger = logging.getLogger(__name__)

# Publication-quality matplotlib style
plt.rcParams.update({
    "figure.dpi": 150,
    "figure.figsize": (10, 6),
    "font.family": "serif",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "legend.frameon": False,
})

PALETTE = ["#2c7bb6", "#d7191c", "#1a9641", "#fdae61", "#756bb1"]


class ModelEvaluator:
    """
    Evaluation, explainability, and visualisation for the project.

    Parameters
    ----------
    config : dict
        Project config (figures path, SHAP settings)
    """

    def __init__(self, config: dict):
        self.config = config
        self.figures_path = Path(config["paths"]["figures"])
        self.figures_path.mkdir(parents=True, exist_ok=True)
        self.shap_max_display = config["evaluation"]["shap_max_display"]

    def _save(self, fig: plt.Figure, name: str):
        path = self.figures_path / f"{name}.png"
        fig.savefig(path, bbox_inches="tight", dpi=150)
        logger.info(f"Saved figure → {path}")
        plt.close(fig)
        return path

    # ------------------------------------------------------------------
    # Event Study Plots
    # ------------------------------------------------------------------

    def plot_car(
        self,
        car_df: pd.DataFrame,
        title: str = "Cumulative Abnormal Returns Around Event",
        show_significance: bool = True,
        save_name: str = "car_plot",
    ) -> plt.Figure:
        """
        Plot CAR over event window with confidence bands and significance markers.

        Parameters
        ----------
        car_df : pd.DataFrame
            Output of EventStudy.run_event_study() — columns: t, mean_AR, mean_CAR, se_AR
        """
        fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        # --- Abnormal Returns ---
        ax1 = axes[0]
        ax1.bar(
            car_df["t"],
            car_df["mean_AR"] * 100,
            color=[PALETTE[0] if v >= 0 else PALETTE[1] for v in car_df["mean_AR"]],
            alpha=0.8,
            label="Mean AR",
        )
        ci = 1.96 * car_df["se_AR"] * 100
        ax1.errorbar(car_df["t"], car_df["mean_AR"] * 100, yerr=ci, fmt="none",
                     color="black", capsize=3, linewidth=0.8, alpha=0.6)
        ax1.axhline(0, color="black", linewidth=0.8, linestyle="--")
        ax1.axvline(0, color="grey", linewidth=1.5, linestyle=":", label="Event day (t=0)")
        ax1.set_ylabel("Abnormal Return (%)")
        ax1.set_title(title, fontsize=13, fontweight="bold")
        ax1.legend()

        # Significance stars
        if show_significance and "significant_05" in car_df.columns:
            for _, row in car_df.iterrows():
                if row["significant_05"]:
                    ax1.annotate(
                        "*", xy=(row["t"], row["mean_AR"] * 100 + ci.max() * 0.1),
                        ha="center", fontsize=12, color="darkred",
                    )

        # --- Cumulative AR ---
        ax2 = axes[1]
        ax2.plot(car_df["t"], car_df["mean_CAR"] * 100,
                 color=PALETTE[0], linewidth=2, marker="o", markersize=4, label="Mean CAR")
        ax2.fill_between(
            car_df["t"],
            (car_df["mean_CAR"] - 1.96 * car_df["se_AR"]) * 100,
            (car_df["mean_CAR"] + 1.96 * car_df["se_AR"]) * 100,
            alpha=0.2, color=PALETTE[0], label="95% CI",
        )
        ax2.axhline(0, color="black", linewidth=0.8, linestyle="--")
        ax2.axvline(0, color="grey", linewidth=1.5, linestyle=":")
        ax2.set_xlabel("Days Relative to Event (t=0)")
        ax2.set_ylabel("Cumulative Abnormal Return (%)")
        ax2.legend()

        fig.tight_layout()
        self._save(fig, save_name)
        return fig

    # ------------------------------------------------------------------
    # SHAP Explainability
    # ------------------------------------------------------------------

    def shap_summary(
        self,
        model,
        X: pd.DataFrame,
        save_name: str = "shap_summary",
    ) -> None:
        """
        Generate SHAP beeswarm summary plot for a tree-based model.

        Parameters
        ----------
        model : fitted XGBoost / LightGBM model
        X : pd.DataFrame — feature matrix (sample or full test set)
        """
        try:
            import shap
        except ImportError:
            raise ImportError("Install shap: pip install shap")

        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

        fig, ax = plt.subplots(figsize=(10, 8))
        shap.summary_plot(
            shap_values,
            X,
            max_display=self.shap_max_display,
            show=False,
        )
        plt.title("SHAP Feature Importance — Market Impact Model", fontweight="bold")
        self._save(plt.gcf(), save_name)

    def shap_waterfall(
        self,
        model,
        X: pd.DataFrame,
        idx: int = 0,
        save_name: str = "shap_waterfall",
    ) -> None:
        """SHAP waterfall plot for a single prediction."""
        try:
            import shap
        except ImportError:
            raise ImportError("Install shap: pip install shap")

        explainer = shap.TreeExplainer(model)
        explanation = explainer(X)
        shap.waterfall_plot(explanation[idx], max_display=15, show=False)
        self._save(plt.gcf(), save_name)

    # ------------------------------------------------------------------
    # Model Comparison
    # ------------------------------------------------------------------

    def plot_model_comparison(
        self,
        results: Dict,
        metric: str = "cv_rmse_mean",
        save_name: str = "model_comparison",
    ) -> plt.Figure:
        """Bar chart comparing models on a given metric."""
        names = list(results.keys())
        values = [results[n][metric] for n in names]
        errors = [results[n].get("cv_rmse_std", 0) for n in names]

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(names, values, color=PALETTE[:len(names)], alpha=0.85)
        ax.errorbar(names, values, yerr=errors, fmt="none", color="black",
                    capsize=5, linewidth=1.2)

        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(errors) * 0.5,
                    f"{val:.4f}", ha="center", va="bottom", fontsize=10, fontweight="bold")

        ax.set_title(f"Model Comparison — {metric.replace('_', ' ').title()}", fontweight="bold")
        ax.set_ylabel(metric.replace("_", " ").title())
        fig.tight_layout()
        self._save(fig, save_name)
        return fig

    def plot_predictions(
        self,
        y_true: pd.Series,
        y_pred: np.ndarray,
        model_name: str = "XGBoost",
        save_name: str = "predictions_vs_actual",
    ) -> plt.Figure:
        """Scatter plot of predicted vs actual returns."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Scatter
        ax1 = axes[0]
        ax1.scatter(y_true, y_pred, alpha=0.4, color=PALETTE[0], s=15)
        lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
        ax1.plot(lims, lims, "k--", linewidth=1, label="Perfect prediction")
        ax1.set_xlabel("Actual Return")
        ax1.set_ylabel("Predicted Return")
        ax1.set_title(f"{model_name} — Predicted vs Actual", fontweight="bold")
        ax1.legend()

        # Time-series of residuals
        ax2 = axes[1]
        residuals = np.array(y_true) - y_pred
        ax2.plot(residuals, color=PALETTE[1], alpha=0.7, linewidth=0.8)
        ax2.axhline(0, color="black", linewidth=0.8, linestyle="--")
        ax2.set_xlabel("Observation Index")
        ax2.set_ylabel("Residual (Actual − Predicted)")
        ax2.set_title("Residuals over Time", fontweight="bold")

        fig.tight_layout()
        self._save(fig, save_name)
        return fig
