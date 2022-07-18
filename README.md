# Central Database

The central database is a smart, scalable and extensible data warehouse that unifies, cleans, enriches and turns data available.

## central_database

This is a Django microservice built with [django-cookiecutter](https://cookiecutter-django.readthedocs.io/en/latest/index.html).
The parameters used to create this project can be found in [cookiecutter.json](cookiecutter.json).

Use the following commands to build and run a local development environment with Docker:

```bash
cd central_database
sudo docker-compose -f local.yml build
sudo docker-compose -f local.yml up