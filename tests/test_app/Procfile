# Used for our heroku deploy (Not needed for development)

release: python manage.py migrate
web: gunicorn library.wsgi -b 0.0.0.0:$PORT --log-file -
