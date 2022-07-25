# Central Database

The central database is a smart, scalable and extensible data warehouse that unifies, cleans, enriches and turns data available.

## central_database

This is a Django microservice built with [django-cookiecutter](https://cookiecutter-django.readthedocs.io/en/latest/index.html).
The parameters used to create this project can be found in [cookiecutter.json](cookiecutter.json).

## Development setup

The project is intended to be developed inside a containerized development environment using Visual Studio Code [Remote - Containers extension](https://code.visualstudio.com/docs/remote/containers). More information on how to develop using containers is available [here](https://www.youtube.com/watch?v=KFyRLxiRKAc).

To open the development IDE, press 'F1' then search for: 'Remote-Containers: Rebuild and Reopen in Container'.
VSCode should reopen your IDE inside the dev container, which should make you ready to start developing! This development image is accompanied by a PostgreSQL database configured (see the file .devcontainer/docker-compose.yml). The database starts with a superuser with username and password 'admin' for you to use.

Use the Run and Debug tab to launch the local Django microservice. Tests should be available in the Testing tab.
