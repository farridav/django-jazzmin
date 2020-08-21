# Used for our heroku deploy (Not needed for development)

release: python tests/test_app/manage.py migrate
web: gunicorn tests.test_app.wsgi -b 0.0.0.0:$PORT --log-file -
