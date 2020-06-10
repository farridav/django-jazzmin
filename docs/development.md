# Development

See [installation](./installation.md) on how to get the project installed for development

Run the test project with

    python tests/test_app/manage.py migrate
    python tests/test_app/manage.py runserver_plus

## Testing
Tests are run on any pull request into `master`, and are written for use with the [pytest](https://docs.pytest.org/en/latest/) 
framework, we should have good enough tests for you to base your own off of, though where we are lacking, or where we have 
skeleton tests, feel free to contribute, but keep it clean, concise and simple, leave the magic to the wizards.

Run tests with `pytest` or target an individual test with `pytest -k my_test_name`

## Contributing
To contribute, fork the project, make a pull request against this repo, include tests unless its a trivial change, 
add a screenshot if your proposing UI changes.
