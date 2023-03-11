#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Perform database migrations
python manage.py migrate

# Start the application server
gunicorn ECOM.wsgi:application --bind 0.0.0.0:$PORT
