# Environmental Sustainability: An Explainable AI Framework for Assessing the Impact of Thermal Power Generation and Coal Production on Air Quality Index (AQI) in India Using Public Government Data

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Research status](https://img.shields.io/badge/status-data%20audit%20in%20progress-orange.svg)](#repository-status)

## Project overview

This master's AIML capstone develops a reproducible public-data framework for examining how **thermal power generation** and **coal production/mining activity** are associated with monthly Air Quality Index (AQI) across **Maharashtra, Gujarat, and Odisha**. It combines statistical models, machine-learning models, and explainable-AI methods with explicit data-quality and monitoring-coverage controls.

The project is designed for environmental decision support. It identifies **associations, predictive relationships, and model explanations**; it does **not** claim plant-level causality, formal emissions attribution, or source apportionment.

## Environmental-sustainability motivation

Reliable state-level evidence can help environmental and energy agencies understand whether industrial activity, weather, seasonality, population structure, and monitoring coverage jointly improve the explanation and prediction of monthly AQI. A transparent workflow is especially important because public datasets differ in format, geographic granularity, temporal coverage, and redistribution terms. This repository therefore emphasizes provenance, auditability, conservative interpretation, and reproducibility before model complexity.

## Research scope

| Element | Scope |
|---|---|
| Unit of analysis | State-month |
| Selected states | Maharashtra, Gujarat, Odisha |
| Selected industries | Thermal power generation; coal production and mining activity |
| Primary target | Monthly mean AQI (`aqi_mean`) |
| Alternative target | Monthly median AQI (`aqi_median`) |
| Preferred period | January 2019 through December 2023, a five-year period |
| Preferred sample | 180 state-month observations: 3 states x 60 months |
| Conservative minimum | 150 complete state-month observations across all research questions |
| Study design | Observational, ecological, predictive, and non-causal |

The final common analytical period may change after the data audit if the official sources do not provide adequate overlapping coverage. If fewer than 150 complete observations remain after alignment, the analysis will reduce the predictor count, simplify the model set, and document the limitation.

## Intended users

The primary intended users are the Maharashtra Pollution Control Board, Gujarat Pollution Control Board, and Odisha State Pollution Control Board. Secondary users include state environment departments, state energy departments, environmental sustainability analysts, academic researchers, public-policy analysts, and industry environmental-compliance teams.

## Research questions and hypotheses

Full wording is maintained in [`docs/research_questions.md`](docs/research_questions.md).

### RQ1

**Question:** To what extent are thermal power generation and coal production individually and jointly associated with monthly AQI across Maharashtra, Gujarat, and Odisha after controlling for weather, population density, state, and season?

- **H0:** Thermal power generation and coal production are not significantly associated with monthly AQI after controls.
- **Ha:** At least one of the two industrial drivers is significantly associated with monthly AQI after controls.

### RQ2

**Question:** Do lagged thermal power generation and coal production indicators improve the explanation and prediction of monthly AQI compared with contemporaneous indicators alone?

- **H0:** Lagged industrial indicators do not improve model fit or predictive performance over contemporaneous indicators alone.
- **Ha:** At least one lagged industrial indicator improves model fit or predictive performance.

### RQ3

**Question:** Which industrial and environmental drivers make the largest and most stable contributions to monthly AQI predictions according to explainable artificial intelligence methods?

- **H0:** Explainability methods do not identify stable high-importance industrial or environmental drivers.
- **Ha:** Explainability methods identify one or more stable high-importance AQI drivers.

### RQ4

**Question:** Do machine-learning models provide materially better out-of-sample AQI predictions than statistical and seasonal baseline models while retaining sufficient interpretability for environmental decision support?

- **H0:** Machine-learning models do not materially outperform statistical or seasonal baseline models.
- **Ha:** At least one machine-learning model materially outperforms the baseline while maintaining interpretable results.

## Variables

### Industrial drivers

- State-month thermal power generation
- State-month coal production or the best available official coal-activity proxy
- One- and two-month lags of both drivers

### Controls

- Monthly rainfall
- Monthly mean temperature
- Monthly relative humidity, where available
- Population density
- State indicators
- Month or seasonal indicators
- Monitoring-station count and station coverage rate

### Secondary air-quality variables

PM2.5, PM10, NO2, SO2, CO, O3, monthly median AQI, and—only if the observed class distribution supports it—an AQI-risk category for a secondary classification task. Proposed definitions and missing-value rules are in [`docs/data_dictionary.csv`](docs/data_dictionary.csv).

## Official public government data sources

Only public government sources are approved for the core analysis.

| Domain | Government source | Official link | Planned use |
|---|---|---|---|
| AQI and pollutants | Central Pollution Control Board / data.gov.in | [Historical Daily Ambient Air Quality Data](https://www.data.gov.in/catalog/historical-daily-ambient-air-quality-data) | AQI, pollutants, station-day records |
| AQI API | Central Pollution Control Board / data.gov.in | [Real-Time Air Quality Index](https://www.data.gov.in/catalog/real-time-air-quality-index) and [API resource](https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69) | Supplemental acquisition and source verification |
| Thermal power | National Power Portal | [Published Reports](https://npp.gov.in/publishedReports) | State-month thermal generation |
| Coal | Coal Controller's Organisation / Ministry of Coal | [Coal Production](https://coalcontroller.gov.in/coal-production) | State-month coal production or best official proxy |
| Weather | India Meteorological Department | [Free Data Access](https://dsp.imdpune.gov.in/home_freedataaccess.php) | Rainfall, temperature, humidity where available |
| Population | Census of India | [Census Data](https://censusindia.gov.in/census.website/en/data) | Population density |

Source status, access method, local path, and redistribution notes are maintained in [`docs/data_source_log.csv`](docs/data_source_log.csv). Coverage must be verified from downloaded files before any source is marked available in [`docs/data_availability_matrix.csv`](docs/data_availability_matrix.csv). Kaggle, private vendor data, and non-government datasets are excluded from the core analysis.

## Analytical framework

The detailed plan is in [`docs/methodology.md`](docs/methodology.md). The implemented workflow covers:

1. Official-source verification, provenance logging, and raw-file inventory.
2. Schema validation, date parsing, state-name standardization, and plausibility checks.
3. Station-day to state-month AQI aggregation, including mean, median, pollutant summaries, station count, and monitoring coverage.
4. Missing-data profiling, duplicate detection, outlier review, unit verification, temporal alignment, and common-period selection.
5. One- and two-month industrial lags, month/season/year features, state indicators, and train-only scaling or imputation.
6. Naive seasonal baseline, multiple linear regression, Ridge, LASSO, random forest regression, and gradient boosting regression.
7. Chronological train-validation-test splitting and rolling or expanding-window validation where the verified sample supports it.
8. Residual diagnostics, multicollinearity checks, state-specific error analysis, and sensitivity analyses.
9. Policy-oriented interpretation with explicit ecological, measurement, and non-causal limitations.

Final models are not trained unless a real processed dataset is present.

## Explainable-AI strategy

[`src/models/explain.py`](src/models/explain.py) supports SHAP TreeExplainer for compatible tree models, permutation importance as a fallback, partial dependence, global ranking, local prediction explanations, state-level comparisons, validation-period comparisons, and explanation-stability tables. Model explanations will be compared across folds or time windows rather than relying on one ranking.

SHAP values and feature importance explain how a fitted model uses available variables. They do not prove causal contribution, plant-level responsibility, or source apportionment.

## Evaluation metrics

The primary regression metrics are:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R-squared
- Adjusted R-squared
- Mean Absolute Percentage Error (MAPE) only when actual AQI values are nonzero and the percentage interpretation is appropriate

Precision, recall, and F1 score are implemented for an optional secondary classification task only if AQI-risk categories have adequate support. Metric implementations and tests are in [`src/models/evaluate.py`](src/models/evaluate.py) and [`tests/test_metrics.py`](tests/test_metrics.py).

## Repository structure

```text
environmental-sustainability-aqi-framework/
├── README.md
├── LICENSE
├── CITATION.cff
├── CONTRIBUTING.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── .env.example
├── Makefile
├── config/
│   └── project_config.yaml
├── data/
│   ├── README.md
│   ├── raw/
│   │   ├── aqi_cpcb/
│   │   ├── power_npp/
│   │   ├── coal_controller/
│   │   ├── weather_imd/
│   │   └── census/
│   ├── interim/
│   └── processed/
├── docs/
│   ├── data_source_log.csv
│   ├── data_dictionary.csv
│   ├── data_availability_matrix.csv
│   ├── methodology.md
│   ├── research_questions.md
│   └── github_screenshot_instructions.md
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_data_cleaning_and_harmonization.ipynb
│   ├── 03_statistical_analysis.ipynb
│   ├── 04_machine_learning.ipynb
│   └── 05_explainability.ipynb
├── src/
│   ├── config.py
│   ├── logging_utils.py
│   ├── data/
│   ├── features/
│   ├── models/
│   └── visualization/
├── tests/
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── models/
├── reports/
│   ├── week3_data_audit_template.md
│   └── progress_report_1_outline.md
└── scripts/
    ├── run_data_audit.py
    ├── build_state_month_panel.py
    └── run_baseline_models.py
```

## Setup

### 1. Clone and enter the repository

```bash
git clone https://github.com/VenkataArunSrinivas/environmental-sustainability-aqi-framework.git
cd environmental-sustainability-aqi-framework
```

### 2. Create a Python 3.11+ virtual environment

**macOS or Linux**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The equivalent Make target is:

```bash
make setup
```

### 4. Configure optional API access

```bash
cp .env.example .env
```

Add a data.gov.in key to the local `.env` only when needed. The `.env` file is ignored by Git. Never commit API keys or credentials.

## Data placement

No fabricated observations or redistributed raw government files are included. Download files directly from the official sources, record the access date and status in [`docs/data_source_log.csv`](docs/data_source_log.csv), and place them as follows:

```text
data/raw/aqi_cpcb/          CPCB or data.gov.in AQI and pollutant files
data/raw/power_npp/         National Power Portal thermal-generation reports
data/raw/coal_controller/   Coal Controller or Ministry of Coal files
data/raw/weather_imd/       IMD rainfall, temperature, and humidity files
data/raw/census/            Census population-density tables
```

Preserve original filenames when possible. CSV and Excel files are supported by the current loaders. Source-specific column names may require documented alias updates after the first audit. Raw files remain ignored by Git.

## Run the workflow

### Data audit

```bash
make audit
# or
python scripts/run_data_audit.py
```

The audit command succeeds gracefully when folders are empty, lists the missing source groups, and writes a local audit summary under `outputs/tables/`.

### Build the state-month panel

```bash
make harmonize
# or
python scripts/build_state_month_panel.py
```

The panel is written to `data/processed/state_month_panel.csv` only after the required source groups are present, source columns can be mapped, and the harmonized data pass validation.

### Run baseline models

```bash
make baseline
# or
python scripts/run_baseline_models.py
```

Model training is skipped with an informative warning when no verified processed panel exists.

### Run tests

```bash
make test
# or
python -m pytest
```

### Clean generated local artifacts

```bash
make clean
```

## Reproducibility notes

- Python package versions are bounded in `requirements.txt` and `pyproject.toml`.
- The default random seed is 42.
- Paths are resolved relative to the repository root; no personal absolute path is hardcoded.
- Scaling and imputation are fitted on training observations only.
- Primary evaluation uses chronological splits rather than random shuffling.
- Industrial lags use prior months within the same state.
- The data-audit notebook runs without failure when raw folders are empty.
- Generated models, processed data, figures, and tables are ignored by Git unless intentionally reviewed for release.
- Source URLs, access dates, formats, local paths, terms, and audit status are tracked separately from analytical output.

## Data licensing and redistribution

The [MIT License](LICENSE) applies to original code and documentation in this repository. Government datasets and third-party publications remain governed by their original source terms. This repository does not grant a new license for CPCB, data.gov.in, National Power Portal, Coal Controller, IMD, Census of India, or any other third-party data. Verify redistribution rights before publishing raw or derived files.

## Limitations

- The study is observational and aggregated at the state-month level.
- Industrial activity may be measured with proxies whose units and geographic allocation require source verification.
- Monitoring networks differ across states and time; station coverage is therefore included as a quality control but may not remove all measurement bias.
- Weather and population controls may not capture all relevant confounders.
- State-level aggregation can obscure local exposure patterns and plant-specific impacts.
- A five-year, three-state panel is modest for complex machine-learning models; the 150-observation minimum is a conservative threshold, not a guarantee of statistical power.
- Missingness, source revisions, inconsistent formats, and limited common coverage may require a shorter final period or simpler model set.
- Predictive importance is not equivalent to causal or policy importance.

## Ethical considerations

The framework avoids fabricated data, protects credentials, documents provenance, and separates verified evidence from planned variables. Results should be reported with uncertainty and without stigmatizing communities, workers, companies, or states. Policy interpretation must acknowledge unequal monitoring coverage and should not imply regulatory fault or plant-level responsibility without source-specific emissions and causal evidence.

## Citation

Use the metadata in [`CITATION.cff`](CITATION.cff). Suggested repository citation:

> Nibhanupudi, V. A. S. (2026). *Environmental Sustainability: An Explainable AI Framework for Assessing the Impact of Thermal Power Generation and Coal Production on Air Quality Index (AQI) in India Using Public Government Data* (Version 0.1.0) [Computer software]. GitHub.

No DOI is claimed.

## Academic details

- **Student:** Venkata Arun Srinivas Nibhanupudi
- **Course:** QM640: Data Analytics Capstone
- **Institution:** Walsh College
- **Mentor:** Mr. Jainesh Garg
- **Term:** Term 3
- **Repository:** [VenkataArunSrinivas/environmental-sustainability-aqi-framework](https://github.com/VenkataArunSrinivas/environmental-sustainability-aqi-framework)

## Repository status

**Week 3: Data collection, literature search, source documentation, and data audit in progress.**

The repository contains the framework, templates, tests, and reproducibility controls. It does not claim that data collection, final model training, or substantive results are complete.

## Contributing and screenshot evidence

Development guidance is in [`CONTRIBUTING.md`](CONTRIBUTING.md). Faculty-ready screenshot steps are in [`docs/github_screenshot_instructions.md`](docs/github_screenshot_instructions.md).
