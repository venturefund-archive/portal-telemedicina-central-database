How to contribute to **<PROJECT_NAME>**
=================================================

Thank you for your interest in contributing to the **<PROJECT_NAME>** - a UNICEF initiative to **<PROJECT_MISSION>**!

This page explains forms of contribution, how to set up the project locally, how to submit a pull-request, create issues and much more.

## Types of contribution

<!--
#TODO: Describe which forms of contribution are welcome (code, bug reporting, documentation, blog posts...).
-->

## How to create a development environment

### Pre-requisites

- [Visual Studio Code](https://code.visualstudio.com/) editor
- [Docker](https://www.docker.com/get-started/) for your operating system
- [Git](https://git-scm.com/downloads)

### Clone repository

`git clone git@bitbucket.org:ptmtech/central-database.git`

### Remote Container

The project is intended to be developed inside a containerized development environment using Visual Studio Code [Remote - Containers extension](https://code.visualstudio.com/docs/remote/containers). More information on how to develop using containers is available [here](https://www.youtube.com/watch?v=KFyRLxiRKAc).

To use the development IDE, open the project folder with VS Code and press 'F1', then search for: 'Remote-Containers: Rebuild and Reopen in Container'.
VS Code should reopen your IDE inside the dev container, which should make you ready to start developing!

Tests should be available in the Testing tab (troubleshooting below). Debug tab also contains a flake8 and a runserver action.

Rebuild and Reopen in Container should create:

- A Django microservice on [localhost:8000](http://localhost:8000/)

- A HL7 FHIR API on [localhost:8080](http://localhost:8080/)

- Documentation on [localhost:9000](http://localhost:9000/)

### Load FHIR synthetic data

[Synthetic data](data/synthetic/synthea/) of 1015 children (0 - 15 years-old) was generated with the [Synthea](https://github.com/synthetichealth/synthea) patient generator. To load the data using the FHIR API, run the `postSynthea.py` script in a terminal **outside the devcontainer environment**:

```bash
cd data/synthetic/synthea
unzip fhir.zip
python postSynthea.py
```

A [mock Bundle](data/synthetic/indicators_proposal/John_Doe_cfsb1660843138275.fhir.json) was also generated to illustrate the ideal structure of FHIR resources for calculating indicators. This Bundle can be loaded using the [HAPI FHIR Server interface](http://localhost:8080/) > Server Actions > Transaction. Alternatively, a Bundle can also be loaded by doing a POST to the [server base](http://localhost:8080/fhir).

### Managing dependencies

This project uses [Poetry](https://python-poetry.org/) for dependency management.
Poetry offers a lockfile to ensure repeatable installs.

To `add` a dependency, use:

```bash
poetry add <package>
```

Use the `--dev` option to add a package as a development dependency only.

The `add` command adds required packages to the pyproject.toml, updates poetry.lock and installs them.

Please consult [Poetry documentation](https://python-poetry.org/docs/) for more information.

### Troubleshooting

#### Tests are not showing in the Test Explorer UI.

The following message appears in VS Code:

>Cannot activate the 'Python Test Explorer for Visual Studio Code' extension because it depends on the 'Python' extension, which is not installed. Would you like to install the extension and reload the window?

Hit the Install and Reload button below the message. The IDE will reopen and tests should now appear in the Test Explorer.

## How to submit a pull-request

<!--
#TODO: Finish up this section
-->

## Code style and good-practices

<!--
#TODO: Finish up this section
-->

## Code review process

<!--
#TODO: Finish up this section
-->
