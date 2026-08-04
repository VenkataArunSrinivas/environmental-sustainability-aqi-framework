"""Baseline and candidate regression models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


@dataclass(frozen=True)
class ModelSpec:
    name: str
    estimator: Any


def preprocessing(categorical: list[str], numeric: list[str]) -> ColumnTransformer:
    return ColumnTransformer(
        [
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
            (
                "numeric",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler()),
                    ]
                ),
                numeric,
            ),
        ],
        remainder="drop",
    )


def candidate_models(random_state: int = 640) -> list[ModelSpec]:
    return [
        ModelSpec("Linear regression", LinearRegression()),
        ModelSpec("Ridge regression", Ridge(alpha=1.0)),
        ModelSpec("LASSO regression", Lasso(alpha=0.01, max_iter=10000)),
        ModelSpec(
            "Random forest",
            RandomForestRegressor(
                n_estimators=300,
                max_depth=6,
                min_samples_leaf=5,
                random_state=random_state,
                n_jobs=-1,
            ),
        ),
        ModelSpec(
            "Gradient boosting",
            GradientBoostingRegressor(
                n_estimators=150,
                max_depth=2,
                learning_rate=0.04,
                random_state=random_state,
            ),
        ),
    ]


def make_pipeline(spec: ModelSpec, categorical: list[str], numeric: list[str]) -> Pipeline:
    return Pipeline([("preprocess", preprocessing(categorical, numeric)), ("model", spec.estimator)])


def chronological_split(frame: pd.DataFrame, holdout_start: str, month_column: str = "month") -> tuple[pd.DataFrame, pd.DataFrame]:
    boundary = pd.Timestamp(holdout_start)
    train = frame[pd.to_datetime(frame[month_column]) < boundary].copy()
    test = frame[pd.to_datetime(frame[month_column]) >= boundary].copy()
    if train.empty or test.empty:
        raise ValueError(f"Chronological split produced an empty partition at {boundary.date()}.")
    return train, test
