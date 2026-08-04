"""Descriptive summaries and publication-ready figures."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def _save(fig: plt.Figure, path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(destination, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return destination


def plot_records_by_state(summary: pd.DataFrame, path: str | Path) -> Path:
    fig, axis = plt.subplots(figsize=(7.2, 4.6))
    axis.bar(summary["state"], summary["records"])
    axis.set_title("Collected Station-Day Air-Quality Records by State")
    axis.set_ylabel("Station-day records")
    for index, value in enumerate(summary["records"]):
        axis.text(index, value, f"{int(value):,}", ha="center", va="bottom", fontsize=9)
    return _save(fig, path)


def plot_all_missing(summary: pd.DataFrame, path: str | Path) -> Path:
    fig, axis = plt.subplots(figsize=(7.2, 4.6))
    axis.bar(summary["state"], summary["all_pollutants_missing_pct"])
    axis.set_title("Rows With All Six Pollutant Fields Missing")
    axis.set_ylabel("Percent of station-day rows")
    axis.set_ylim(0, 100)
    for index, value in enumerate(summary["all_pollutants_missing_pct"]):
        axis.text(index, value, f"{value:.1f}%", ha="center", va="bottom", fontsize=9)
    return _save(fig, path)


def plot_monthly_valid_records(cleaned: pd.DataFrame, path: str | Path) -> Path:
    monthly = (
        cleaned.assign(any_pollutant=~cleaned["all_pollutants_missing"])
        .groupby(["month", "state"])["any_pollutant"]
        .sum()
        .unstack("state")
        .sort_index()
    )
    fig, axis = plt.subplots(figsize=(9.2, 4.8))
    for state in monthly.columns:
        axis.plot(monthly.index, monthly[state], marker="o", linewidth=1.4, markersize=3, label=state)
    axis.set_title("Monthly Rows With at Least One Valid Pollutant Value")
    axis.set_xlabel("Month")
    axis.set_ylabel("Valid station-day rows")
    axis.legend()
    axis.tick_params(axis="x", rotation=45)
    return _save(fig, path)


def plot_particulate_medians(cleaned: pd.DataFrame, path: str | Path) -> Path:
    summary = cleaned.groupby("state")[["PM2.5", "PM10"]].median().sort_index()
    fig, axis = plt.subplots(figsize=(7.2, 4.6))
    summary.plot(kind="bar", ax=axis)
    axis.set_title("Preliminary Particulate-Matter Medians by State")
    axis.set_ylabel("Reported field value; source units require verification")
    axis.set_xlabel("")
    axis.tick_params(axis="x", rotation=0)
    return _save(fig, path)


def plot_valid_station_months(station_month: pd.DataFrame, path: str | Path) -> Path:
    values = station_month.groupby("state")["aqi_ready_valid75"].sum().sort_index()
    fig, axis = plt.subplots(figsize=(7.2, 4.6))
    axis.bar(values.index, values.values)
    axis.set_title("Station-Months Passing the 75% Provisional AQI-Readiness Rule")
    axis.set_ylabel("Valid station-months")
    for index, value in enumerate(values.values):
        axis.text(index, value, f"{int(value):,}", ha="center", va="bottom", fontsize=9)
    return _save(fig, path)


def plot_baseline_performance(metrics: pd.DataFrame, path: str | Path) -> Path:
    fig, axis = plt.subplots(figsize=(7.2, 4.6))
    axis.bar(metrics["model"], metrics["rmse"])
    axis.set_title("Interim PM2.5 Pipeline Smoke-Test Performance")
    axis.set_ylabel("RMSE on chronological holdout")
    axis.tick_params(axis="x", rotation=15)
    for index, value in enumerate(metrics["rmse"]):
        axis.text(index, value, f"{value:.2f}", ha="center", va="bottom", fontsize=9)
    return _save(fig, path)


def plot_source_coverage_timeline(coverage: pd.DataFrame, path: str | Path) -> Path:
    fig, axis = plt.subplots(figsize=(9.2, 4.8))
    y_positions = range(len(coverage))
    for y, row in zip(y_positions, coverage.itertuples(index=False)):
        axis.plot([row.start_date, row.end_date], [y, y], linewidth=8, solid_capstyle="butt")
    axis.set_yticks(list(y_positions), coverage["source"])
    axis.set_title("Current Source Coverage and Continuity")
    axis.set_xlabel("Calendar date")
    axis.grid(axis="x", alpha=0.25)
    return _save(fig, path)
