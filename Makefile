PYTHON = python3
VENV = .venv
VENV_BIN = $(VENV)/bin
VENV_ACTIVATE = $(VENV_BIN)/activate

SOURCES = $(wildcard dango/*.py tests/*.py)

.PHONY: default
default: $(VENV)

$(VENV_ACTIVATE): setup.py
	@$(PYTHON) -m venv $(VENV)
	@$(VENV_BIN)/pip install -e .[test]

.PHONY: tests
tests: $(VENV_ACTIVATE)
	@$(VENV_BIN)/pytest

.coverage: $(VENV_ACTIVATE) $(SOURCES) .coveragerc pytest.ini
	@$(VENV_BIN)/coverage run -m pytest

htmlcov/index.html: .coverage
	@$(VENV_BIN)/coverage html

.PHONY: coverage
coverage: .coverage
	@$(VENV_BIN)/coverage report -m

.PHONY: coverage-html
coverage-html: htmlcov/index.html
