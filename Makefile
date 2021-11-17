PYTHON = python3
VENV = .venv
VENV_BIN = $(VENV)/bin
VENV_ACTIVATE = $(VENV_BIN)/activate
COVERAGE_HTML = htmlcov/index.html

SOURCES = $(wildcard dango/*.py tests/*.py)

.PHONY: default
default: $(VENV)

$(VENV_ACTIVATE): setup.py
	@$(PYTHON) -m venv $(VENV)
	@$(VENV_BIN)/pip install -e .[dev,test]

.coverage: $(VENV_ACTIVATE) $(SOURCES) .coveragerc pytest.ini
	@$(VENV_BIN)/coverage run -m pytest

$(COVERAGE_HTML): .coverage
	@$(VENV_BIN)/coverage html

.PHONY: test
test: $(VENV_ACTIVATE)
	@$(VENV_BIN)/pytest

.PHONY: coverage
coverage: .coverage $(COVERAGE_HTML)
	@$(VENV_BIN)/coverage report -m

.PHONY: lint
lint:
	@$(VENV_BIN)/flake8 dango tests

.PHONY: type-check
type-check:
	@$(VENV_BIN)/mypy dango tests

.PHONY: install
install: $(VENV_ACTIVATE)
