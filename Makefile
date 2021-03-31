.PHONY: clean clean-test clean-pyc clean-build docs help
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

ifndef BUCKET
BUCKET	:= eu-west-1.files.compose-x.io
endif

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr src/dist
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint:	confiorm ## check style with flake8
	flake8 cfn_kafka_topic_provider tests

test: ## run tests quickly with the default Python
	pytest

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source cfn_kafka_topic_provider -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/cfn_kafka_topic_provider.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ cfn_kafka_topic_provider
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

conform	: ## Conform to a standard of coding syntax
	black setup.py cfn_kafka_topic_provider tests

dist: clean ## builds source and wheel package
	cd src; python setup.py sdist
	cd src; python setup.py bdist_wheel
	ls -l src/dist

package: dist
	rm -rf build function.zip; mkdir build
	pip install src/dist/ews_kafka_topic*.whl -t build/
# 	cd build ; zip -qr9 ../function.zip *

upload:	package
	aws cloudformation package \
	--s3-bucket $(BUCKET) \
	--s3-prefix aws_cfn_provider_ews_kafka_topic \
	--template-file cfn-kafka-provider-function.yaml \
	--output-template-file function.yaml

deploy: upload
	aws cloudformation deploy --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
	--template-file function.yaml \
	--stack-name cfn-kafka-provider-function

publish: package deploy
