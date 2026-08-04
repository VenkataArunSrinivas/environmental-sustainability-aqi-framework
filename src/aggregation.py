"""Station-month and state-month aggregation."""
from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


def station_month_panel(
    frame: pd.DataFrame,
    completeness_threshold: float = 0.75,
    provisional_aqi_column: str = "aqi_provisional",
) -> pd.DataFrame:
    """Aggregate cleaned station-day records and calculate explicit coverage rates."""
    required = {"state", "city", "station", "month", "date", "PM2.5", "PM10"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Station-month aggregation is missing columns: {sorted(missing)}")
    aggregations: dict[str, tuple[str, str]] = {
        "raw_rows": ("date", "size"),
        "pm25_days": ("PM2.5", "count"),
        "pm25_mean": ("PM2.5", "mean"),
        "pm25_median": ("PM2.5", "median"),
        "pm10_days": ("PM10", "count"),
        "pm10_mean": ("PM10", "mean"),
        "pm10_median": ("PM10", "median"),
    }
    if "aqi_ready_provisional" in frame.columns:
        aggregations["aqi_ready_days"] = ("aqi_ready_provisional", "sum")
    if provisional_aqi_column in frame.columns:
        aggregations["aqi_provisional_mean"] = (provisional_aqi_column, "mean")
        aggregations["aqi_provisional_median"] = (provisional_aqi_column, "median")

    result = (
        frame.groupby(["state", "city", "station", "month"], dropna=False)
        .agg(**aggregations)
        .reset_index()
    )
    result["expected_days"] = result["month"].dt.days_in_month
    result["pm25_coverage_rate"] = result["pm25_days"] / result["expected_days"]
    result["pm10_coverage_rate"] = result["pm10_days"] / result["expected_days"]
    result["pm25_valid75"] = result["pm25_coverage_rate"] >= completeness_threshold
    result["pm10_valid75"] = result["pm10_coverage_rate"] >= completeness_threshold
    if "aqi_ready_days" in result.columns:
        result["aqi_ready_coverage_rate"] = result["aqi_ready_days"] / result["expected_days"]
        result["aqi_ready_valid75"] = result["aqi_ready_coverage_rate"] >= completeness_threshold
    return result


def state_month_summary(
    station_month: pd.DataFrame,
    validity_column: str = "aqi_ready_valid75",
    value_columns: Sequence[str] = ("aqi_provisional_median", "pm25_median", "pm10_median"),
) -> pd.DataFrame:
    """Summarize valid station-months without calling the result an official state AQI."""
    if validity_column not in station_month.columns:
        raise ValueError(f"Validity column not available: {validity_column}")
    valid = station_month[station_month[validity_column]].copy()
    available_values = [column for column in value_columns if column in valid.columns]
    named: dict[str, tuple[str, str]] = {
        "station_count": ("station", "nunique"),
        "city_count": ("city", "nunique"),
    }
    for column in available_values:
        named[column] = (column, "median")
    return valid.groupby(["state", "month"], dropna=False).agg(**named).reset_index()
