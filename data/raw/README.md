# Data directory

The repository separates source files from derived analytical artifacts.

- `data/raw/aqi_cpcb/`: original air-quality workbooks, retained unchanged.
- `data/raw/power_npp/coal/`: original monthly coal statements.
- `data/raw/power_npp/thermal/`: original thermal-generation reports.
- `data/interim/`: reproducible data-audit outputs. Files containing provisional AQI diagnostics are labeled explicitly.
- `data/processed/`: final harmonized modeling panel after industrial and weather validation.

Raw files should be committed only when the source terms permit redistribution. When a raw file cannot be redistributed, record its official URL, download date, local file name, checksum, schema, and acquisition instructions in `docs/data_source_log.xlsx`.

## Required final input schemas

`data/processed/industrial_state_month.csv` must contain a unique `state,month` key and validated fields such as `thermal_generation_gwh` and `coal_consumption_kt`.

`data/processed/weather_state_month.csv` must contain a unique `state,month` key and validated controls such as `rainfall_mm`, `temperature_c`, and, when available, `humidity_pct`.
