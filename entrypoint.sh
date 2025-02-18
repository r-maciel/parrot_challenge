#!/bin/sh
echo "Running migrations"
python manage.py migrate

echo "Creating default superuser"
python manage.py createsuperuser --noinput

echo "Initializing server"
exec "$@"
