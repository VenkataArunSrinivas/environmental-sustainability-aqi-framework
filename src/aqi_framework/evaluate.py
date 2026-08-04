"""Model evaluation metrics."""
from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def regression_metrics(y_true: Iterable[float], y_pred: Iterable[float]) -> dict[str, float]:
    truth = np.asarray(list(y_true), dtype=float)
    prediction = np.asarray(list(y_pred), dtype=float)
    return {
        "mae": float(mean_absolute_error(truth, prediction)),
        "rmse": float(mean_squared_error(truth, prediction) ** 0.5),
        "r2": float(r2_score(truth, prediction)),
    }


def jaccard_top_k(first: Iterable[str], second: Iterable[str], k: int = 5) -> float:
    a = set(list(first)[:k])
    b = set(list(second)[:k])
    union = a | b
    return float(len(a & b) / len(union)) if union else 1.0


def metrics_frame(rows: list[dict[str, object]]) -> pd.DataFrame:
    return pd.DataFrame(rows)
