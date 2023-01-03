#!/bin/bash

echo Running migrations...

python central_database/manage.py migrate
