#!/bin/sh

sleep 10

python manage.py makemigrations
python manage.py migrate
python manage.py createcachetable
python manage.py collectstatic  --noinput

exec "$@"