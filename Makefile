PYTHON ?= python

.PHONY: install audit interim test panel models clean

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -e .

audit:
	PYTHONPATH=src $(PYTHON) scripts/run_data_audit.py --config config/project_config.yaml

interim:
	PYTHONPATH=src $(PYTHON) scripts/run_interim_analysis.py --config config/project_config.yaml --allow-provisional-aqi

test:
	PYTHONPATH=src $(PYTHON) -m pytest

panel:
	PYTHONPATH=src $(PYTHON) scripts/build_harmonized_panel.py --config config/project_config.yaml

models:
	PYTHONPATH=src $(PYTHON) scripts/run_baseline_models.py --config config/project_config.yaml

clean:
	rm -f data/interim/*.csv data/processed/*.csv outputs/tables/*.csv outputs/figures/*.png
