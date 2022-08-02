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

- A fhirbase basic Web UI for querying database on [localhost:3005](http://localhost:3005/)

- Documentation on [localhost:9000](http://localhost:9000/)

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