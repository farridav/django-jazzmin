CYAN ?= \033[0;36m
COFF ?= \033[0m

.PHONY: deps lint check test help test_app
.EXPORT_ALL_VARIABLES:

.DEFAULT: help
help: ## Display help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(CYAN)%-30s$(COFF) %s\n", $$1, $$2}'

# Check whether there is a poetry env and it is a directory (env info may persist even after removing env)
environment := $(shell [ -d "$$(poetry env info -p)" ] && echo "poetry run")

check-venv:
	$(if $(environment),, $(error No poetry environment found, either run "make deps" or "poetry install"))

deps: ## Install dependencies
	@printf "$(CYAN)Updating python deps$(COFF)\n"
	pip3 install -U pip poetry
	poetry install

lint: check-venv ## Lint the code
	@printf "$(CYAN)Auto-formatting with ruff$(COFF)\n"
	$(environment) ruff format jazzmin tests
	$(environment) ruff check jazzmin tests --fix

check: check-venv ## Check code quality
	@printf "$(CYAN)Running static code analysis$(COFF)\n"
	$(environment) ruff format --check jazzmin tests
	$(environment) ruff check jazzmin tests
	$(environment) mypy jazzmin tests --ignore-missing-imports

test: check-venv ## Run the test suite
	@printf "$(CYAN)Running test suite$(COFF)\n"
	$(environment) pytest

reset_app: check-venv ## Reset the DB for a fresh install.
	@printf "$(CYAN)Resetting the local DB$(COFF)\n"
	$(environment) python tests/test_app/manage.py reset

test_app: check-venv ## Run the test app
	@printf "$(CYAN)Running test app$(COFF)\n"
	$(environment) python tests/test_app/manage.py migrate  # Setup db tables etc.
	$(environment) python tests/test_app/manage.py runserver_plus  # Run development server (with werkzeug debugger).

test_user:  ## Make the test user
	$(environment) python tests/test_app/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('test@test.com', password='test')"
