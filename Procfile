release: python manage.py migrate --noinput
web: gunicorn config.wsgi:application --workers 1
