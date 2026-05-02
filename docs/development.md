# Development

## Installation

This project manages dependencies using [uv](https://docs.astral.sh/uv/)

Ensure you have uv installed (see [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/))

Then get setup:

    git clone git@github.com:farridav/django-jazzmin.git
    cd django-jazzmin
    make deps

## Running the test project

Setup db tables etc.

    uv run python tests/test_app/manage.py migrate

Generate test data

    uv run python tests/test_app/manage.py reset

Run development server (with werkzeug debugger)

    uv run python tests/test_app/manage.py runserver_plus

Or simply use the Makefile:

    make test_app

## Running the tests

Tests are run via github actions on any pull request into `main`, and are written for use with the [pytest](https://docs.pytest.org/en/latest/)
framework, we should have good enough tests for you to base your own off of, though where we are lacking, feel free to contribute,
but keep it clean, concise and simple, leave the magic to the wizards.

Run the test suite with `make test` or target an individual test
with `uv run pytest -k my_test_name`

## Contribution guidelines

- Fork the project
- Make a pull request against this repositories `main` branch,
- Include tests unless its a trivial change
- Add a screenshot if your proposing UI changes
- Demonstrate the change within the `test_app` if possible
- No breaking changes please

## Coding guidelines

- autoformat your code with `make lint` (uses [ruff](https://docs.astral.sh/ruff/))
- When fixing something display related, please bear the following in mind:
  - Try fixing the problem using HTML, else CSS, else JS
  - Try removing code, else changing code, else adding code

## Serving documentation locally

You can serve the docs locally using `mkdocs serve -a localhost:8001` and visiting [http://localhost:8001](http://localhost:8001)

## Translations

Working with translations in jazzmin is, a bit unorthodox, as we are overriding djangos templates, so it looks like we have a lot of strings that need translating,
but in-fact they already have translation strings in Django, heres the process for dealing with translations, though we recommend not adding new strings that need
translating if possible, and use suitable iconography instead (See [Font Awesome 5.13.0 free icons](https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2)),
or use a string that is already translated upstream in Django.

### Adding a new language

1. cd into the jazzmin folder
2. Add the desired language directory e.g mkdir -p locale/de/LC_MESSAGES
3. Run django-admin makemessages
4. cd ../
5. Run ./cli.py locales --prune de to remove the django provided strings
6. Go through the strings in the locale file, any that are not genuinely new strings introduced by jazzmin, find them in the codebase, and try making them match the ones provided in djangos admin/admin docs translation files
    - [Django admin docs translations example for German language](https://raw.githubusercontent.com/django/django/main/django/contrib/admin/locale/de/LC_MESSAGES/django.po)

Once you have finished, run `makemessages` again, until the file contains ONLY unique strings to jazzmin, there should only be a handful
