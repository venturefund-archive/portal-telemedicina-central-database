#!/bin/bash

echo Running migrations...

python manage.py migrate

echo Updating static files...
python /app/manage.py collectstatic --noinput
