#!/bin/sh
set -e
python manage.py migrate --noinput
python manage.py seed_demo || true
gunicorn apps.config.wsgi:application --bind 0.0.0.0:38503
