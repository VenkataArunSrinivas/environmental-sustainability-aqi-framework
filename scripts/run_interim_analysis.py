#!/usr/bin/env python
"""Reproduce interim data audit, EDA figures, and a clearly labeled PM2.5 pipeline smoke test."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.linear_model import Ridge

from aqi_framework.aggregation import state_month_summary, station_month_panel
from aqi_framework.aqi import add_provisional_aqi
from aqi_framework.cleaning import clean_air_quality, quality_summary
from aqi_framework.config import load_config
from aqi_framework.eda import (
    plot_all_missing,
    plot_baseline_performance,
    plot_monthly_valid_records,
    plot_particulate_medians,
    plot_records_by_state,
    plot_source_coverage_timeline,
    plot_valid_station_months,
)
from aqi_framework.evaluate import regression_metrics
from aqi_framework.io import read_air_quality_collection, write_csv
from aqi_framework.models import ModelSpec, chronological_split, make_pipeline


def pm25_smoke_test(station_month: pd.DataFrame, holdout_start: str) -> pd.DataFrame:
    """Verify the chronological modeling code; not a final sector-impact model."""
    data = station_month[station_month["pm25_valid75"] & station_month["pm25_median"].notna()].copy()
    data = data.sort_values(["state", "station", "month"])
    data["previous_month"] = data.groupby(["state", "station"])["month"].shift(1)
    data["previous_pm25"] = data.groupby(["state", "station"])["pm25_median"].shift(1)
    data["is_consecutive"] = [
        (current.to_period("M") - prior.to_period("M")).n == 1 if pd.notna(prior) else False
        for current, prior in zip(data["month"], data["previous_month"])
    ]
    data["month_number"] = data["month"].dt.month.astype(str)
    train, test = chronological_split(data, holdout_start)

    rows: list[dict[str, object]] = []
    persistence = test[test["is_consecutive"] & test["previous_pm25"].notna()].copy()
    if not persistence.empty:
        rows.append(
            {
                "model": "Previous-month persistence",
                "target": "PM2.5 field median",
                "train_n": len(train),
                "test_n": len(persistence),
                **regression_metrics(persistence["pm25_median"], persistence["previous_pm25"]),
                "interpretive_status": "Pipeline smoke test; not a final RQ4 result",
            }
        )

    categorical = ["state", "station", "month_number"]
    numeric = ["pm25_coverage_rate"]
    specification = ModelSpec("Location-season Ridge", Ridge(alpha=1.0))
    pipeline = make_pipeline(specification, categorical, numeric)
    pipeline.fit(train[categorical + numeric], train["pm25_median"])
    prediction = pipeline.predict(test[categorical + numeric])
    rows.append(
        {
            "model": specification.name,
            "target": "PM2.5 field median",
            "train_n": len(train),
            "test_n": len(test),
            **regression_metrics(test["pm25_median"], prediction),
            "interpretive_status": "Pipeline smoke test; industrial and weather drivers absent",
        }
    )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/project_config.yaml")
    parser.add_argument("--allow-provisional-aqi", action="store_true")
    args = parser.parse_args()
    config = load_config(args.config)

    raw = read_air_quality_collection(config.path("paths.aqi_raw_dir"), config.get("files.aqi_workbooks"))
    cleaned = clean_air_quality(raw, config.get("quality.pollutant_columns"))
    cleaned = add_provisional_aqi(
        cleaned,
        pollutants=config.get("quality.pollutant_columns"),
        minimum_pollutants=int(config.get("quality.minimum_pollutants_for_provisional_aqi")),
        require_particulate=bool(config.get("quality.require_pm_for_provisional_aqi")),
        allow_provisional=args.allow_provisional_aqi,
    )
    station_month = station_month_panel(cleaned, float(config.get("quality.station_month_completeness")))
    state_month = state_month_summary(station_month)
    audit = quality_summary(cleaned, config.get("quality.pollutant_columns"))
    baseline = pm25_smoke_test(station_month, str(config.get("modeling.holdout_start")))

    interim_dir = config.path("paths.interim_dir")
    tables_dir = config.path("paths.tables_dir")
    figures_dir = config.path("paths.figures_dir")
    for directory in (interim_dir, tables_dir, figures_dir):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(cleaned, interim_dir / "station_day_clean_with_provisional_diagnostic.csv")
    write_csv(station_month, interim_dir / "station_month_summary.csv")
    write_csv(state_month, interim_dir / "state_month_monitoring_summary.csv")
    write_csv(audit, tables_dir / "air_quality_audit_summary.csv")
    write_csv(baseline, tables_dir / "preliminary_pm25_smoke_test_metrics.csv")

    readiness = (
        station_month.groupby("state")
        .agg(
            station_months=("station", "size"),
            aqi_ready_valid75=("aqi_ready_valid75", "sum"),
            pm25_valid75=("pm25_valid75", "sum"),
            median_aqi_ready_coverage=("aqi_ready_coverage_rate", "median"),
        )
        .reset_index()
    )
    write_csv(readiness, tables_dir / "station_month_readiness.csv")

    plot_records_by_state(audit, figures_dir / "fig01_records_by_state.png")
    plot_all_missing(audit, figures_dir / "fig02_all_pollutants_missing.png")
    plot_monthly_valid_records(cleaned, figures_dir / "fig03_monthly_valid_records.png")
    plot_particulate_medians(cleaned, figures_dir / "fig04_particulate_medians.png")
    plot_valid_station_months(station_month, figures_dir / "fig05_valid_station_months.png")
    plot_baseline_performance(baseline, figures_dir / "fig06_preliminary_baseline_performance.png")

    coverage = pd.DataFrame(
        [
            {"source": "Air-quality workbooks", "start_date": pd.Timestamp("2021-08-01"), "end_date": pd.Timestamp("2023-07-31")},
            {"source": "Coal statements currently collected", "start_date": pd.Timestamp("2023-04-01"), "end_date": pd.Timestamp("2026-01-31")},
            {"source": "Thermal reports currently collected", "start_date": pd.Timestamp("2021-01-01"), "end_date": pd.Timestamp("2023-01-31")},
        ]
    )
    plot_source_coverage_timeline(coverage, figures_dir / "fig07_source_coverage_timeline.png")
    write_csv(coverage, tables_dir / "source_coverage_timeline.csv")
    print(f"Interim analysis complete. Valid station-months: {int(station_month['aqi_ready_valid75'].sum())}")


if __name__ == "__main__":
    main()
