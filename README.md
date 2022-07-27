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
```



# Fhirbase

<<<<<<< HEAD
<!-- **[Download the Latest Release](https://github.com/fhirbase/fhirbase/releases/)**&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;**[Try Online](https://fbdemo.aidbox.app/)**&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;[Documentation](https://aidbox.gitbook.io/fhirbase/)&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;[Chat](https://chat.fhir.org/#narrow/stream/16-fhirbase)&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;[Google Group](https://groups.google.com/forum/#!forum/fhirbase)

[![Build Status](https://travis-ci.org/fhirbase/fhirbase.svg?branch=master)](https://travis-ci.org/fhirbase/fhirbase) -->

Fhirbase is a command-line utility which enables you to easily import
[FHIR data](https://www.hl7.org/fhir/) into a PostgreSQL database and
work with it in a relational way. Also Fhirbase provides set of stored
procedures to perform [CRUD
operations](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)
and maintain [Resources
History](https://www.hl7.org/fhir/http.html#history).

<p align="center">
    <img src="https://cdn.rawgit.com/fhirbase/fhirbase/a6aff815/demo/asciicast.svg" />
</p>

## Status

Server FHIR running on a docker container with the the purpose to bring a PoC

## Requirements

To run the FHIR server - Docker Container you must have **Docker** installed on you computer

## Getting Started

to run the application just run:  **docker run --rm -p 3000:3000 fhirbase/fhirbase:latest** and go to **http://localhost:3000**

## Usage Statistics



## Development


## License

=======
The central database is a smart, scalable and extensible data warehouse that unifies, cleans, enriches and turns data available.

## central_database

This is a Django microservice built with [django-cookiecutter](https://cookiecutter-django.readthedocs.io/en/latest/index.html).
The parameters used to create this project can be found in [cookiecutter.json](cookiecutter.json).

## Development setup

The project is intended to be developed inside a containerized development environment using Visual Studio Code [Remote - Containers extension](https://code.visualstudio.com/docs/remote/containers). More information on how to develop using containers is available [here](https://www.youtube.com/watch?v=KFyRLxiRKAc).

To open the development IDE, press 'F1' then search for: 'Remote-Containers: Rebuild and Reopen in Container'.
VSCode should reopen your IDE inside the dev container, which should make you ready to start developing! This development image is accompanied by a PostgreSQL database configured (see the file .devcontainer/docker-compose.yml). The database starts with a superuser with username and password 'admin' for you to use.

Use the Run and Debug tab to launch the local Django microservice. Tests should be available in the Testing tab.

## Troubleshooting

### Tests and not showing in the Test Explorer UI.
The following message appears in VS Code:
>Cannot activate the 'Python Test Explorer for Visual Studio Code' extension because it depends on the 'Python' extension, which is not installed. Would you like to install the extension and reload the window?

Hit the Install and Reload button below the message. The IDE will reopen and tests should now appear in the Test Explorer.
>>>>>>> feat/DevContainer
