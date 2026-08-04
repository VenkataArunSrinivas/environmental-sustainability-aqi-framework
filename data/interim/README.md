# Interim derived data

- `station_day_clean_sample.csv` is a 1,000-row review sample, not the complete analysis table.
- `station_month_summary.csv` contains the derived station-month summaries used for interim readiness checks.
- `state_month_monitoring_summary.csv` contains network-level state-month summaries.
- `interim_data_summary.xlsx` consolidates key audit tables for evaluator review.

The complete station-day derived table is intentionally not included in the upload package because it is large and is reproducible from the original workbooks already present in the target GitHub repository. Run `python scripts/run_interim_analysis.py --config config/project_config.yaml --allow-provisional-aqi` to recreate it. The provisional AQI diagnostic is not an official AQI series.
