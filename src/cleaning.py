"""Auditable cleaning and quality-control operations."""
from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd

DEFAULT_POLLUTANTS = ["Ozone", "CO", "SO2", "NO2", "PM10", "PM2.5"]
STATE_ALIASES = {
    "Maharasthra": "Maharashtra",
    "Orissa": "Odisha",
}


def clean_air_quality(frame: pd.DataFrame, pollutants: Sequence[str] = DEFAULT_POLLUTANTS) -> pd.DataFrame:
    """Standardize dates, states, strings, and pollutant numeric fields.

    Missing pollutant values are deliberately retained as missing; they are never
    replaced with zero.
    """
    result = frame.copy()
    result["date"] = pd.to_datetime(result["From Date"], dayfirst=True, errors="coerce")
    result["to_date"] = pd.to_datetime(result["To Date"], dayfirst=True, errors="coerce")
    result["state"] = result["State"].astype("string").str.strip().replace(STATE_ALIASES)
    result["city"] = result["City"].astype("string").str.strip()
    result["station"] = result["Station"].astype("string").str.strip()
    for pollutant in pollutants:
        result[pollutant] = pd.to_numeric(result[pollutant], errors="coerce")
        result.loc[result[pollutant] < 0, pollutant] = np.nan
    result["month"] = result["date"].dt.to_period("M").dt.to_timestamp()
    result["valid_pollutant_count"] = result[list(pollutants)].notna().sum(axis=1)
    result["has_particulate"] = result[["PM10", "PM2.5"]].notna().any(axis=1)
    result["all_pollutants_missing"] = result[list(pollutants)].isna().all(axis=1)
    result["record_key"] = (
        result["state"].fillna("")
        + "|"
        + result["city"].fillna("")
        + "|"
        + result["station"].fillna("")
        + "|"
        + result["date"].astype("string").fillna("")
    )
    return result


def exact_duplicate_count(frame: pd.DataFrame) -> int:
    return int(frame.duplicated().sum())


def station_date_duplicate_count(frame: pd.DataFrame) -> int:
    keys = ["state", "city", "station", "date"]
    return int(frame.duplicated(subset=keys).sum())


def quality_summary(frame: pd.DataFrame, pollutants: Sequence[str] = DEFAULT_POLLUTANTS) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for state, group in frame.groupby("state", dropna=False):
        record: dict[str, object] = {
            "state": state,
            "records": len(group),
            "cities": group["city"].nunique(dropna=True),
            "stations": group["station"].nunique(dropna=True),
            "date_min": group["date"].min(),
            "date_max": group["date"].max(),
            "all_pollutants_missing_n": int(group["all_pollutants_missing"].sum()),
            "all_pollutants_missing_pct": 100 * float(group["all_pollutants_missing"].mean()),
        }
        for pollutant in pollutants:
            record[f"{pollutant}_missing_pct"] = 100 * float(group[pollutant].isna().mean())
        rows.append(record)
    return pd.DataFrame(rows).sort_values("state").reset_index(drop=True)
