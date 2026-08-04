#!/usr/bin/env python
"""Build the final panel only after industrial and weather inputs are available."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from aqi_framework.config import load_config
from aqi_framework.io import write_csv


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/project_config.yaml")
    args = parser.parse_args()
    config = load_config(args.config)

    station_month_path = config.path("paths.interim_dir") / "station_month_summary.csv"
    industrial_path = config.path("paths.industrial_monthly")
    weather_path = config.path("paths.weather_monthly")
    missing = [path for path in (station_month_path, industrial_path, weather_path) if not path.exists()]
    if missing:
        joined = "\n - ".join(str(path) for path in missing)
        raise FileNotFoundError(
            "The final panel cannot be built until these required files exist:\n - " + joined
            + "\nRun the interim audit first, then populate the documented industrial and weather schemas."
        )

    station_month = pd.read_csv(station_month_path, parse_dates=["month"])
    industrial = pd.read_csv(industrial_path, parse_dates=["month"])
    weather = pd.read_csv(weather_path, parse_dates=["month"])
    for name, frame in {"industrial": industrial, "weather": weather}.items():
        required = {"state", "month"}
        absent = required.difference(frame.columns)
        if absent:
            raise ValueError(f"{name} input is missing merge keys: {sorted(absent)}")
        if frame.duplicated(subset=["state", "month"]).any():
            raise ValueError(f"{name} input has duplicate state-month keys; resolve before merging.")

    panel = station_month.merge(industrial, on=["state", "month"], how="inner", validate="many_to_one")
    panel = panel.merge(weather, on=["state", "month"], how="inner", validate="many_to_one")
    destination = config.path("paths.processed_dir") / "harmonized_station_month_panel.csv"
    write_csv(panel, destination)
    print(f"Wrote {len(panel):,} rows to {destination}")


if __name__ == "__main__":
    main()
