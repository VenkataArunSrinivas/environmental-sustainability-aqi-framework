# Contributing

Contributions that improve reproducibility, validation, documentation, or
government-data ingestion are welcome.

## Development workflow

1. Create a branch from `main`.
2. Create and activate a Python 3.11 or newer virtual environment.
3. Install development dependencies with `pip install -e ".[dev]"`.
4. Add or update tests for behavioral changes.
5. Run `pytest` before opening a pull request.
6. Keep raw source files, credentials, model binaries, and generated outputs out
   of commits.

## Data integrity

Never fabricate observations or present simulated data as official data. Any
new source used for the core analysis must be a public Government of India or
state-government source and must be documented in `docs/data_source_log.csv`.
Source-specific terms of use remain controlling.

## Research claims

Code and documentation must describe associations, predictions, and model
explanations. Do not convert these results into plant-level causal claims or
formal source-apportionment conclusions.
