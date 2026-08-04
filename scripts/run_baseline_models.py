#!/usr/bin/env python
"""Run final baseline/candidate models after the harmonized panel exists."""
from __future__ import annotations

import argparse

import pandas as pd

from aqi_framework.config import load_config
from aqi_framework.evaluate import regression_metrics
from aqi_framework.features import assert_no_aqi_component_leakage
from aqi_framework.io import write_csv
from aqi_framework.models import candidate_models, chronological_split, make_pipeline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/project_config.yaml")
    parser.add_argument("--target", default=None)
    args = parser.parse_args()
    config = load_config(args.config)
    panel_path = config.path("paths.processed_dir") / "harmonized_station_month_panel.csv"
    if not panel_path.exists():
        raise FileNotFoundError(f"Run build_harmonized_panel.py first: {panel_path}")
    panel = pd.read_csv(panel_path, parse_dates=["month"])
    target = args.target or next((name for name in config.get("modeling.target_preference") if name in panel.columns), None)
    if target is None:
        raise ValueError("No configured target is present in the harmonized panel.")

    categorical = [column for column in ["state", "station", "season"] if column in panel.columns]
    numeric = [
        column
        for column in [
            "thermal_generation_gwh",
            "coal_consumption_kt",
            "rainfall_mm",
            "temperature_c",
            "humidity_pct",
            "aqi_ready_coverage_rate",
        ]
        if column in panel.columns
    ]
    assert_no_aqi_component_leakage(categorical + numeric, target)
    train, test = chronological_split(panel.dropna(subset=[target]), str(config.get("modeling.holdout_start")))
    rows = []
    for specification in candidate_models(int(config.get("modeling.random_state"))):
        model = make_pipeline(specification, categorical, numeric)
        model.fit(train[categorical + numeric], train[target])
        prediction = model.predict(test[categorical + numeric])
        rows.append({"model": specification.name, "target": target, "train_n": len(train), "test_n": len(test), **regression_metrics(test[target], prediction)})
    destination = config.path("paths.tables_dir") / "final_model_comparison.csv"
    write_csv(pd.DataFrame(rows), destination)
    print(f"Wrote model comparison to {destination}")


if __name__ == "__main__":
    main()
