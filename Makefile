PYTHON ?= python

.PHONY: setup audit harmonize baseline test clean

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"

audit:
	$(PYTHON) scripts/run_data_audit.py

harmonize:
	$(PYTHON) scripts/build_state_month_panel.py

baseline:
	$(PYTHON) scripts/run_baseline_models.py

test:
	$(PYTHON) -m pytest

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find outputs/figures outputs/tables outputs/models -type f ! -name ".gitkeep" -delete
	find data/interim data/processed -type f ! -name ".gitkeep" -delete
