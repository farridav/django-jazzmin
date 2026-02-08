# Django-Jazzmin: Agent & Developer Guidelines

This document defines coding rules and best practices for Python package development, with a focus on Django packages. Follow these when editing the codebase.

---

## Python package development

### Tooling and workflow
- **Use the Makefile** for all standard tasks: `make deps`, `make lint`, `make check`, `make test`
- **Before committing:** run `make lint`, `make check`, and `make test` (or rely on CI)
- **Prefer `uv`** for dependency management and running commands: `uv run <command>` for scripts and tools
- **Keep `pyproject.toml` authoritative:** dependency ranges, classifiers, and tool config live here; avoid duplicating in other config files
- **Lockfile:** commit `uv.lock` for reproducible installs

### Dependencies and code reuse
- **Prefer third-party libraries** over implementing behavior ourselves when a maintained package exists and fits the need
- **Pin only in the lockfile;** use lower-bounded version ranges in `pyproject.toml` (e.g. `django>=4.2`) so users get compatible updates
- **Dev-only dependencies** belong in `[dependency-groups] dev`, not in `[project.dependencies]`

### Documentation and style
- **Use multi-line docstrings** for all public modules, classes, and functions (even one-liners)
- **Keep `requires-python` and Trove classifiers** in sync with what we actually test and support (see CI matrix and docs)

---

## Django package development

### App and integration
- **Provide a clear AppConfig** and document how to add the app to `INSTALLED_APPS`
- **Use Django’s public APIs and extension points** (middleware, template tags, admin hooks, static/template discovery); avoid relying on private or undocumented internals
- **Templates and static files:** use Django’s app directory convention so `APP_DIRS = True` and `collectstatic` discover them without extra config
- **Default settings:** provide sensible defaults; document any required or commonly overridden settings (e.g. in README or docs)

### Compatibility and upgrades
- **Support the Django and Python versions** declared in `pyproject.toml` and CI; when dropping support, update classifiers, `requires-python`, and dependency bounds
- **Handle deprecations:** fix or gate code that triggers Django deprecation warnings in supported versions; avoid leaving deprecated code paths in place when we no longer support older series
- **Test against the supported matrix** (Python 3.10–3.13 and recent Django 4.2, 5.x, 6.x) so changes don’t break advertised compatibility

### Backward compatibility
- **Avoid breaking existing projects:** prefer additive or optional behavior; if a setting or API must change, document it and consider a deprecation path before removing or changing behavior

---

## Code style & philosophy

### Avoid over-abstraction
- **Prefer simple functions over classes** when classes don’t add value
- **Avoid unnecessary abstraction layers** — if the Django ORM can do it directly, use it
- **Don’t create abstractions “just in case”** — wait until you have a concrete need
- **Favor readability over clever abstractions** — code should be easy to understand

### Testing style
- **Use functional pytest style** — tests as functions, not classes
- **Keep tests clear and readable** with fewer lines of code
- **Store and re-use pytest fixtures** in `conftest.py` unless they are truly test-specific
- **Prefer functional, real-world testing** over meticulous unit testing
- **Use `@pytest.mark.django_db`** (or equivalent) for tests that touch the database

### Error handling
- **Never use `try/except Exception`** over large code blocks
- **Only wrap the specific code** that can raise the exception
- **Use specific exceptions** — catch the exact exception type you expect
- **Avoid catching generic `Exception`** unless there is a documented reason

### Type annotations
- **Use type annotations** for all public APIs and for function arguments and return values; include types inside dicts and lists where it helps
- **Use `TypedDict`** (or similar) when the structure of a dictionary is known
- **Satisfy mypy** for the configured strictness (see `pyproject.toml`)

### Code organization
- **Prefer functions over classes** — use classes when you need state or polymorphism
- **Avoid over-abstraction** — favor readability
- **Keep functions focused** — one clear responsibility per function
- **Use meaningful names** — code should be self-documenting
