#!/bin/bash

echo Running migrations...

python /app/manage.py migrate
