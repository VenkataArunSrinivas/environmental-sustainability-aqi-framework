# Interim Dataset Datasheet

## Motivation
The analytical dataset is being created to evaluate transparent associations and predictions linking thermal-power activity, coal consumption at thermal power stations, meteorology, and monitored air quality in selected Indian states. It is a screening dataset, not a plant-level source-apportionment dataset.

## Composition
The current air-quality component contains 62,780 station-day rows from Gujarat, Maharashtra, and Odisha, covering August 2021 through July 2023. It includes six pollutant fields, state, city, station, and date. AQI is not present in the source workbooks. The current industrial collection is incomplete and is not yet merged.

## Collection Process
Files were obtained from public Government of India portals or official reporting pages and retained unchanged in the raw layer. Download dates, URLs, filenames, and status are recorded in the source log.

## Preprocessing
Dates, state names, numeric types, and missingness indicators are standardized reproducibly. Missing pollutant values are never replaced with zero. Station-month inclusion uses explicit completeness thresholds. A provisional AQI calculation is available only as an opt-in diagnostic and must not be represented as official AQI.

## Uses
Recommended uses: data-quality assessment, descriptive pollutant analysis, chronological modeling after full harmonization, and public-sector screening. Prohibited or unsupported uses: plant-level causal attribution, legal compliance findings, individual health-risk decisions, or comparisons that ignore monitoring coverage.

## Distribution and Maintenance
Original code and permitted derived outputs are public in GitHub. Raw government files are shared only when redistribution is allowed. Version history is maintained through Git commits and release tags.
