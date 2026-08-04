"""Leakage-aware feature engineering."""
from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


def add_calendar_features(frame: pd.DataFrame, month_column: str = "month") -> pd.DataFrame:
    result = frame.copy()
    month = pd.to_datetime(result[month_column])
    result["year"] = month.dt.year
    result["month_number"] = month.dt.month
    result["season"] = month.dt.month.map(
        {
            12: "Winter", 1: "Winter", 2: "Winter",
            3: "Pre-monsoon", 4: "Pre-monsoon", 5: "Pre-monsoon",
            6: "Monsoon", 7: "Monsoon", 8: "Monsoon", 9: "Monsoon",
            10: "Post-monsoon", 11: "Post-monsoon",
        }
    )
    return result


def add_group_lags(
    frame: pd.DataFrame,
    value_columns: Sequence[str],
    group_columns: Sequence[str] = ("state",),
    month_column: str = "month",
    lags: Sequence[int] = (1, 2),
) -> pd.DataFrame:
    result = frame.sort_values([*group_columns, month_column]).copy()
    for column in value_columns:
        for lag in lags:
            result[f"{column}_lag{lag}"] = result.groupby(list(group_columns))[column].shift(lag)
    return result


def assert_no_aqi_component_leakage(features: Sequence[str], target: str) -> None:
    if "aqi" not in target.lower():
        return
    prohibited = {"PM2.5", "PM10", "NO2", "SO2", "CO", "Ozone", "pm25", "pm10", "no2", "so2", "co", "ozone"}
    offenders = [feature for feature in features if any(token.lower() in feature.lower() for token in prohibited)]
    if offenders:
        raise ValueError(f"Same-period pollutant components cannot predict AQI in the primary model: {offenders}")
