PYTHON = python3
VENV = .venv
VENV_BIN = $(VENV)/bin
VENV_ACTIVATE = $(VENV_BIN)/activate
COVERAGE_HTML = htmlcov/index.html
DEV_INSTALL = dango.egg-info

SOURCES = $(wildcard dango/*.py tests/*.py)

.PHONY: default
default: install

$(VENV):
	$(PYTHON) -m venv $(VENV)
	# Make sure pip is up to date as installation of some dependencies depend on that.
	$(VENV_BIN)/python -m pip -v install --upgrade pip

$(DEV_INSTALL): $(VENV) setup.py
	$(VENV_BIN)/pip -v install -e .[dev,test]

.coverage: $(DEV_INSTALL) $(SOURCES) .coveragerc pytest.ini
	$(VENV_BIN)/coverage run -m pytest

$(COVERAGE_HTML): .coverage
	$(VENV_BIN)/coverage html

.PHONY: install
install: $(DEV_INSTALL)

.PHONY: test
test: $(DEV_INSTALL)
	$(VENV_BIN)/pytest

.PHONY: coverage
coverage: .coverage $(COVERAGE_HTML)
	$(VENV_BIN)/coverage report -m

.PHONY: lint
lint: $(DEV_INSTALL)
	$(VENV_BIN)/flake8 dango tests

.PHONY: type-check
type-check: $(DEV_INSTALL)
	$(VENV_BIN)/mypy dango tests

dist: $(VENV) $(SOURCES) pyproject.toml setup.py LICENSE README.md
	$(VENV_BIN)/python -m build

.PHONY: dist-check
dist-check: dist
	$(VENV_BIN)/twine check dist/*

.PHONY: clean
clean:
	-@rm -rf .mypy_cache .pytest_cache .coverage htmlcov dist
