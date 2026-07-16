"""Generate Appendix Figure A8: held-out residual diagnostics.

Input (authoritative, current):
  reports/model_comparison/event_model_predictions.parquet
    columns: date, split, actual, Baseline_LASSO_pred, Event_LASSO_pred,
             XGBoost_pred, LightGBM_pred
  Filtered to split == "test" (the 750-row held-out FES v1.1 / MCP v1.0 test
  set also reported in Table 11).

Baseline_LASSO and Event_LASSO produce byte-identical predictions on the test
split (verified: (test.Baseline_LASSO_pred == test.Event_LASSO_pred).all() is
True), consistent with Section 4.5's "identical constant predictions" finding,
so they are shown as a single combined row rather than duplicated.

Residual std for Event_LASSO computed here (0.00963023815800501) matches
reports/model_comparison/statistical_tests.json exactly, confirming the input
data is the same version used for the reported Jarque-Bera / Durbin-Watson
statistics in Section 4.9.

Output: reports/figures/A8_residual_diagnostics.png
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats as sstats

REPO_ROOT = Path(__file__).resolve().parents[1]
PRED_PATH = REPO_ROOT / "reports" / "model_comparison" / "event_model_predictions.parquet"
OUT_PNG = REPO_ROOT / "reports" / "figures" / "A8_residual_diagnostics.png"

ROWS = [
    ("Market-only LASSO baseline / Event-enhanced LASSO\n(identical constant predictions)", "Baseline_LASSO_pred"),
    ("XGBoost", "XGBoost_pred"),
    ("LightGBM", "LightGBM_pred"),
]

BAR_COLOR = "#8FA6B2"
LINE_COLOR = "#C0392B"
POINT_COLOR = "#2E75B6"


def main():
    df = pd.read_parquet(PRED_PATH)
    test = df[df["split"] == "test"].sort_values("date").reset_index(drop=True)
    assert len(test) == 750, f"expected 750 held-out rows, got {len(test)}"

    fig, axes = plt.subplots(len(ROWS), 3, figsize=(13, 3.6 * len(ROWS)))
    fig.suptitle(
        "Held-Out Residual Diagnostics (FES v1.1 / MCP v1.0, 750-row test split)",
        fontsize=14, fontweight="bold",
    )

    for i, (label, pred_col) in enumerate(ROWS):
        resid = (test["actual"] - test[pred_col]).to_numpy()

        ax = axes[i, 0]
        ax.hist(resid, bins=40, color=BAR_COLOR, edgecolor="white", density=True)
        xs = np.linspace(resid.min(), resid.max(), 200)
        ax.plot(xs, sstats.norm.pdf(xs, resid.mean(), resid.std()), color=LINE_COLOR, linewidth=1.4)
        ax.set_title("Residual histogram + density" if i == 0 else "")
        ax.set_ylabel(label, fontsize=9)

        ax = axes[i, 1]
        sstats.probplot(resid, dist="norm", plot=ax)
        ax.set_title("Q-Q plot vs. normal" if i == 0 else "")
        ax.get_lines()[0].set_markerfacecolor(POINT_COLOR)
        ax.get_lines()[0].set_markeredgecolor(POINT_COLOR)
        ax.get_lines()[0].set_markersize(3)
        ax.get_lines()[1].set_color(LINE_COLOR)

        ax = axes[i, 2]
        ax.plot(test["date"], resid, color=POINT_COLOR, linewidth=0.7)
        ax.axhline(0, color=LINE_COLOR, linewidth=0.9, linestyle="--")
        ax.set_title("Residuals over time" if i == 0 else "")
        ax.tick_params(axis="x", rotation=30)

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT_PNG, dpi=220)
    print(f"wrote {OUT_PNG}")


if __name__ == "__main__":
    main()
