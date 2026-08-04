"""Model-behavior explanation helpers."""
from __future__ import annotations

import pandas as pd
from sklearn.inspection import permutation_importance


def permutation_importance_table(model, features: pd.DataFrame, target: pd.Series, repeats: int = 20, random_state: int = 640) -> pd.DataFrame:
    """Compute held-out permutation importance; values are predictive, not causal."""
    result = permutation_importance(
        model,
        features,
        target,
        n_repeats=repeats,
        random_state=random_state,
        scoring="neg_root_mean_squared_error",
    )
    return (
        pd.DataFrame(
            {
                "feature": features.columns,
                "importance_mean": result.importances_mean,
                "importance_std": result.importances_std,
            }
        )
        .sort_values("importance_mean", ascending=False)
        .reset_index(drop=True)
    )
