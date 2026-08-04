"""Conditional CPCB AQI reconstruction for data-readiness diagnostics.

IMPORTANT: This module is not a substitute for an official reported AQI series.
It may be used only after verifying pollutant units, averaging periods, completeness,
and CPCB method requirements. Interim outputs are explicitly labeled provisional.
"""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd

# Concentration breakpoints and AQI index ranges used for a provisional diagnostic.
# Values must be checked against the official CPCB methodology before final use.
BREAKPOINTS: dict[str, list[tuple[float, float, int, int]]] = {
    "PM10": [(0, 50, 0, 50), (51, 100, 51, 100), (101, 250, 101, 200), (251, 350, 201, 300), (351, 430, 301, 400), (431, 1000, 401, 500)],
    "PM2.5": [(0, 30, 0, 50), (31, 60, 51, 100), (61, 90, 101, 200), (91, 120, 201, 300), (121, 250, 301, 400), (251, 1000, 401, 500)],
    "NO2": [(0, 40, 0, 50), (41, 80, 51, 100), (81, 180, 101, 200), (181, 280, 201, 300), (281, 400, 301, 400), (401, 1000, 401, 500)],
    "SO2": [(0, 40, 0, 50), (41, 80, 51, 100), (81, 380, 101, 200), (381, 800, 201, 300), (801, 1600, 301, 400), (1601, 3000, 401, 500)],
    "CO": [(0, 1, 0, 50), (1.1, 2, 51, 100), (2.1, 10, 101, 200), (10.1, 17, 201, 300), (17.1, 34, 301, 400), (34.1, 100, 401, 500)],
    "Ozone": [(0, 50, 0, 50), (51, 100, 51, 100), (101, 168, 101, 200), (169, 208, 201, 300), (209, 748, 301, 400), (749, 2000, 401, 500)],
}


def subindex(value: float | int | None, pollutant: str) -> float:
    if value is None or pd.isna(value):
        return np.nan
    numeric = float(value)
    if numeric < 0:
        return np.nan
    if pollutant not in BREAKPOINTS:
        raise KeyError(f"No provisional breakpoints configured for {pollutant}")
    for concentration_low, concentration_high, index_low, index_high in BREAKPOINTS[pollutant]:
        if numeric <= concentration_high:
            bounded = max(numeric, concentration_low)
            return ((index_high - index_low) / (concentration_high - concentration_low)) * (
                bounded - concentration_low
            ) + index_low
    return 500.0


def add_provisional_aqi(
    frame: pd.DataFrame,
    pollutants: Sequence[str] = ("Ozone", "CO", "SO2", "NO2", "PM10", "PM2.5"),
    minimum_pollutants: int = 3,
    require_particulate: bool = True,
    allow_provisional: bool = False,
) -> pd.DataFrame:
    """Add provisional subindices and AQI only when explicitly authorized."""
    if not allow_provisional:
        raise RuntimeError(
            "Provisional AQI is disabled. Pass allow_provisional=True only for an explicitly labeled interim diagnostic."
        )
    result = frame.copy()
    readiness = result[list(pollutants)].notna().sum(axis=1) >= minimum_pollutants
    if require_particulate:
        readiness &= result[["PM10", "PM2.5"]].notna().any(axis=1)
    for pollutant in pollutants:
        result[f"{pollutant}_subindex_provisional"] = result[pollutant].map(lambda value: subindex(value, pollutant))
    subindex_columns = [f"{pollutant}_subindex_provisional" for pollutant in pollutants]
    result["aqi_ready_provisional"] = readiness
    result["aqi_provisional"] = result[subindex_columns].max(axis=1, skipna=True)
    result.loc[~readiness, "aqi_provisional"] = np.nan
    return result
