# Environmental Sustainability: An Explainable AI Framework for Assessing Associations Between Thermal Power Generation, Coal Consumption, and Air Quality in Selected Indian States

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Interim%20data%20audit-orange.svg)](#current-project-status)

This Walsh College QM640 Data Analytics Capstone develops a reproducible framework for examining associations between **thermal power generation**, **coal consumption at thermal power stations**, meteorology, and monitored air quality in selected Indian states. The framework combines transparent data auditing, statistical analysis, machine learning, and explainable artificial intelligence. It is a decision-support screening framework and does not claim plant-level causality or formal source apportionment.

## Current project status

The repository is **ready to support the graded Interim Report**, but it is **not final-model ready**.

- Air-quality workbooks collected: Gujarat, Maharashtra, and Odisha.
- Current air-quality inventory: **62,780 station-day rows, 86 stations, and 39 cities**.
- Air-quality file period: **August 2021 through July 2023**, with uneven usable coverage across states.
- The workbooks contain pollutant concentrations but do not contain a reported AQI column.
- Monthly coal-consumption reports are partially collected for selected months.
- Thermal-generation reports are available only for sample months/report types.
- Weather and population-control data are not yet harmonized.
- No final industrial-association or machine-learning performance conclusion is claimed.

The current scope refinements are **provisional and pending mentor review before final model estimation**. See [`docs/scope_change_record.md`](docs/scope_change_record.md).

## Interim analytical scope

| Element | Current working treatment |
|---|---|
| Primary industrial driver 1 | Thermal power generation |
| Primary industrial driver 2 | Coal consumption at thermal power stations |
| Core states | Maharashtra and Gujarat |
| Conditional state | Odisha, subject to common-period and quality criteria |
| Data-search window | 2019–2026 |
| Anticipated common period | Approximately 12–18 contiguous months; not yet confirmed |
| Candidate analytical unit | Station-month air-quality outcomes linked to grouped state-month industrial exposures |
| Preferred outcome | Reported or validated AQI |
| Fallback outcome | PM2.5 or PM10 if AQI cannot be defensibly validated |
| Interpretation | Observational associations and predictive explanations, not causal attribution |

## Intended users

The primary intended users are State Pollution Control Boards and state environment and energy departments. Secondary users include sustainability analysts, academic researchers, public-policy analysts, and industry environmental-compliance teams.

## Research questions

The full research questions, hypotheses, target-definition note, and analytical mapping are documented in [`docs/research_questions.md`](docs/research_questions.md). In summary, the study evaluates:

1. Individual and joint associations of thermal generation and coal consumption with monthly air-quality outcomes after controls.
2. Whether lagged industrial indicators improve explanation or prediction.
3. Which industrial and environmental drivers make the largest and most stable predictive contributions.
4. Whether interpretable machine-learning models improve out-of-sample prediction over statistical and seasonal baselines.

## Data sources and availability

Core sources are restricted to public government data.

| Component | Government source | Current status |
|---|---|---|
| Air quality and pollutants | CPCB / Open Government Data Platform India | Three state workbooks collected and audited |
| Thermal generation | National Power Portal / Central Electricity Authority | Partial sample reports collected |
| Coal consumption, receipt, and stock | National Power Portal / Central Electricity Authority | Selected monthly reports collected |
| Weather | India Meteorological Department | Pending |
| Population and structural controls | Census of India | Pending |

Detailed provenance, URLs, coverage, and next actions are recorded in [`docs/data_source_log.csv`](docs/data_source_log.csv) and [`docs/data_availability_matrix.csv`](docs/data_availability_matrix.csv). Variable definitions are provided in [`docs/data_dictionary.csv`](docs/data_dictionary.csv) and [`docs/data_dictionary.xlsx`](docs/data_dictionary.xlsx).

The current public repository contains the collected source workbooks. These files remain unchanged. Government and third-party source terms continue to apply; the MIT License applies only to original code and documentation.

## Repository structure

```text
config/                 Project configuration and quality thresholds
data/raw/               Original source files and source-specific folders
data/interim/           Reproducible audit and station-month outputs
data/processed/         Final harmonized panel after source validation
docs/                   Source log, dictionary, datasheet, scope, methods, and rubric mapping
notebooks/              Data-audit, cleaning, and modeling walkthroughs
outputs/figures/        Interim figures used in the report
outputs/tables/         Audit, sample-size, and smoke-test tables
reports/                Submission-ready Interim Report PDF and editable source
scripts/                Command-line workflows
src/aqi_framework/      Reusable Python package
tests/                   Automated checks
```

## Setup and validation

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pytest
```

Run the data audit:

```powershell
$env:PYTHONPATH = "src"
python scripts/run_data_audit.py --config config/project_config.yaml
```

Run the interim analysis and explicitly allow the provisional AQI diagnostic:

```powershell
$env:PYTHONPATH = "src"
python scripts/run_interim_analysis.py --config config/project_config.yaml --allow-provisional-aqi
```

The provisional AQI diagnostic is a pipeline check only. It must not be interpreted as official AQI or used for final inference until pollutant units, averaging periods, and CPCB derivation rules are verified.

## Research safeguards

- Raw files are retained unchanged.
- Missing values are not converted to zero.
- Pollutant units and averaging periods must be verified before AQI derivation.
- Same-period pollutant concentrations are not used as predictors of AQI in the primary sector-association model.
- Repeated station observations sharing one state-month industrial exposure are handled as grouped data.
- Validation is chronological and group-aware rather than randomly shuffled at row level.
- SHAP and permutation importance explain fitted-model behavior; they do not establish causality.
- Model complexity will be reduced if the effective sample and unique exposure periods are insufficient.

## Interim report

- [`Environmental_Sustainability_AQI_Interim_Report_Final_v2.pdf`](reports/Environmental_Sustainability_AQI_Interim_Report_Final_v2.pdf)
- [`Environmental_Sustainability_AQI_Interim_Report_Final_v2.docx`](reports/Environmental_Sustainability_AQI_Interim_Report_Final_v2.docx)

## Academic details

- **Student:** Venkata Arun Srinivas Nibhanupudi
- **Institution:** Walsh College
- **Course:** QM640: Data Analytics Capstone
- **Mentor:** Mr. Jainesh Garg
- **Term:** Term 3
- **Repository:** https://github.com/VenkataArunSrinivas/environmental-sustainability-aqi-framework

## License and citation

Original code and documentation are released under the [`MIT License`](LICENSE). Government datasets remain subject to their source terms. Citation metadata are available in [`CITATION.cff`](CITATION.cff).
