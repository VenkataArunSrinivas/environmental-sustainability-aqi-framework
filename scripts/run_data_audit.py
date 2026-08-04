#!/usr/bin/env python
"""Audit collected air-quality and industrial source files without modeling."""
from __future__ import annotations

import argparse
from pathlib import Path

from aqi_framework.cleaning import clean_air_quality, exact_duplicate_count, quality_summary, station_date_duplicate_count
from aqi_framework.config import load_config
from aqi_framework.io import list_source_files, read_air_quality_collection, write_csv
from aqi_framework.sample_size import planning_table


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/project_config.yaml")
    args = parser.parse_args()
    config = load_config(args.config)
    pollutants = config.get("quality.pollutant_columns")
    raw = read_air_quality_collection(config.path("paths.aqi_raw_dir"), config.get("files.aqi_workbooks"))
    cleaned = clean_air_quality(raw, pollutants)

    tables = config.path("paths.tables_dir")
    tables.mkdir(parents=True, exist_ok=True)
    write_csv(quality_summary(cleaned, pollutants), tables / "air_quality_audit_summary.csv")
    write_csv(list_source_files(config.path("paths.coal_raw_dir")), tables / "coal_file_inventory.csv")
    write_csv(list_source_files(config.path("paths.thermal_raw_dir")), tables / "thermal_file_inventory.csv")
    write_csv(__import__("pandas").DataFrame(planning_table()), tables / "sample_size_plan.csv")

    validation = __import__("pandas").DataFrame(
        [
            {"check": "exact_duplicates", "value": exact_duplicate_count(cleaned)},
            {"check": "station_date_duplicates", "value": station_date_duplicate_count(cleaned)},
            {"check": "date_parse_failures", "value": int(cleaned["date"].isna().sum())},
            {"check": "all_pollutants_missing", "value": int(cleaned["all_pollutants_missing"].sum())},
        ]
    )
    write_csv(validation, tables / "validation_checks.csv")
    print(f"Audit complete. Tables written to {tables}")


if __name__ == "__main__":
    main()
