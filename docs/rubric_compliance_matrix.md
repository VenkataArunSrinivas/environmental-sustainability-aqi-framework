# Interim Report Rubric Compliance Matrix

| Rubric criterion | Points | Evidence in report | Supporting repository evidence |
|---|---:|---|---|
| Title Page and APA formatting | 10 | APA 7 student title page; page numbers; consistent headings; numbered and titled tables/figures; in-text citations | `reports/`; `docs/manual_actions_before_submission.md` |
| Introduction, Scope, and Objectives | 15 | Background and Context; Problem Statement; Purpose; Progress Snapshot; Tables 2-4 | `docs/research_questions.md`; `docs/scope_change_record.md` |
| Literature Survey | 20 | Search approach; 14-source relevance matrix; thematic synthesis linking evidence to RQs and design decisions | `docs/methodology.md`; report References |
| Data Description | 20 | Sources and access; dataset inventory; industrial-data status; mandatory data dictionary; GitHub availability statement | `docs/data_source_log.xlsx`; `docs/data_dictionary.xlsx`; `docs/dataset_datasheet.md` |
| Analysis | 65 | Reproducible cleaning workflow; quantitative cleaning log; EDA tables/figures and interpretations; sample-size calculations with parameter reasoning; research workflow | `scripts/run_interim_analysis.py`; `src/aqi_framework/`; `outputs/figures/`; `outputs/tables/`; `data/interim/` |
| Modelling | 30 | Model-selection reasoning; feature set; target-leakage controls; grouped chronological validation; metric formulas | `scripts/run_baseline_models.py`; `src/aqi_framework/models.py`; `features.py`; `evaluate.py`; `explain.py` |
| Preliminary Results | 20 | RQ-by-RQ interim status; PM2.5 smoke-test performance; explicit interpretation and limitations | `outputs/tables/preliminary_pm25_smoke_test_metrics.csv`; Figure 6 |
| Bibliography | 20 | 21 APA-style references, including more than 10 directly relevant scholarly sources and official government sources | `CITATION.cff`; report References |

The matrix is a quality-control aid. It does not replace the evaluator's judgment and must not be inserted into the report unless the template permits it.
