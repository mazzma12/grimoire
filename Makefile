.PHONY: clean clean-build clean-pyc clean-ipynb help install
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"
BUILD_DIR = "_site"
BOLD=$$(tput bold)
NORMAL=$$(tput sgr0)

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

book: clean-build
	jupytext --to qmd posts/*/*.py
	quarto render
	$(BROWSER) $(BUILD_DIR)/index.html

clean: clean-build ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr $(BUILD_DIR)

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-ipynb:
	find . -name '.ipynb_checkpoints' -exec rm -f {} +

install: clean
	pip install -r requirements.txt
