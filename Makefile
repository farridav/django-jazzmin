CYAN ?= \033[0;36m
COFF ?= \033[0m

.PHONY: deps lint check test help test_app test_user build publish publish-test publish-test-only version
.EXPORT_ALL_VARIABLES:

.DEFAULT: help
help: ## Display help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(CYAN)%-30s$(COFF) %s\n", $$1, $$2}'

deps: ## Install dependencies
	@printf "$(CYAN)Updating python deps$(COFF)\n"
	pip3 install -U pip uv
	uv sync --all-groups

lint: ## Lint the code
	@printf "$(CYAN)Auto-formatting with ruff$(COFF)\n"
	uv run ruff format jazzmin tests
	uv run ruff check jazzmin tests --fix

check: ## Check code quality
	@printf "$(CYAN)Running static code analysis$(COFF)\n"
	uv run ruff format --check jazzmin tests
	uv run ruff check jazzmin tests
	uv run mypy jazzmin tests --ignore-missing-imports

test: ## Run the test suite
	@printf "$(CYAN)Running test suite$(COFF)\n"
	uv run pytest

test_app: ## Run the test app
	@printf "$(CYAN)Running test app$(COFF)\n"
	uv run python tests/test_app/manage.py migrate
	uv run python tests/test_app/manage.py runserver_plus

test_user: ## Make the test user
	uv run python tests/test_app/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('test@test.com', password='test')"

build: ## Build the package
	uv build --no-sources

publish: ## Publish to PyPI (set PYPI_TOKEN or pass -p)
	$(MAKE) build
	uv publish --username __token__ --password "$${PYPI_TOKEN}"

publish-test: ## Publish to Test PyPI (set TEST_PYPI_TOKEN or pass -p)
	$(MAKE) build
	uv publish --index testpypi --username __token__ --password "$${TEST_PYPI_TOKEN}"

publish-test-only: ## Publish existing dist/ to Test PyPI (for CI after restoring cached build)
	uv publish --index testpypi --username __token__ --password "$${TEST_PYPI_TOKEN}"

version: ## Set version (e.g. make version VERSION=3.0.3)
	@if [ -z "$(VERSION)" ]; then echo "Usage: make version VERSION=x.y.z"; exit 1; fi
	uv version $(VERSION) --frozen

version-prerelease: ## Bump to next prerelease (for pre-release workflow)
	@LATEST_RELEASE_TEST_PYPI=$$(curl -s https://test.pypi.org/rss/project/django-jazzmin/releases.xml | sed -n 's/\s*<title>\([{a,b}0-9.]*\).*/\1/p' | head -n 2 | xargs); \
	LATEST_RELEASE_GITHUB=$$(curl -s "https://api.github.com/repos/farridav/django-jazzmin/tags" | jq -r '.[0].name[1:]'); \
	LATEST_RELEASE=$$(printf "$${LATEST_RELEASE_GITHUB}\n$${LATEST_RELEASE_TEST_PYPI}" | sort -V -r | head -n 1); \
	uv version $${LATEST_RELEASE} --frozen; \
	uv version --bump patch --bump alpha --frozen


download_bootswatch_css: ## Download the Bootswatch CSS and source map files
	for theme in default brite cerulean cosmo cyborg darkly flatly journal litera lumen lux materia minty morph pulse quartz sandstone simplex sketchy slate solar spacelab superhero united vapor yeti zephyr; do \
		mkdir -p jazzmin/static/vendor/bootswatch/$${theme}; \
		curl -s https://bootswatch.com/5/$${theme}/bootstrap.min.css -o jazzmin/static/vendor/bootswatch/$${theme}/bootstrap.min.css; \
		curl -s https://bootswatch.com/5/$${theme}/bootstrap.min.css.map -o jazzmin/static/vendor/bootswatch/$${theme}/bootstrap.min.css.map; \
	done