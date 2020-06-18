# Development

## Installation

    git clone git@github.com:farridav/django-jazzmin.git
    python3 -m venv .venv
    . .venv/bin/activate
    pip install -r dev-requirements.txt

## Running the test project

Setup db tables etc.

    python tests/test_app/manage.py migrate

Generate test data

    python tests/test_app/manage.py loaddata initial_data

Run development server (with werkzeug debugger)

    python tests/test_app/manage.py runserver_plus

## Running the tests
Tests are run via github actions on any pull request into `master`, and are written for use with the [pytest](https://docs.pytest.org/en/latest/) 
framework, we should have good enough tests for you to base your own off of, though where we are lacking, or where we have 
skeleton tests, feel free to contribute, but keep it clean, concise and simple, leave the magic to the wizards.

Run the test suite with your current python interpreter and Django version using `pytest` or target an individual test 
with `pytest -k my_test_name`

Run against all supported Python and Django Versions using `tox`

## Contribution guidelines
- Fork the project
- Make a pull request against this repos `master` branch, 
- Include tests unless its a trivial change
- Add a screenshot if your proposing UI changes
- No breaking changes please
