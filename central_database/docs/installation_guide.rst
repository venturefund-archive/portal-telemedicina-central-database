How to create a development environment
======================================================================

Pre-requisites
---------------

* Visual Studio Code editor
* Docker for your operating system
* Git

Clone repository
----------------
::

    git clone git@bitbucket.org:ptmtech/central-database.git

Remote Container
-----------------

The project is intended to be developed inside a containerized development environment using Visual Studio Code Remote - Containers extension. More information on how to develop using containers is available here.

To use the development IDE, open the project folder with VS Code and press 'F1', then search for: 'Remote-Containers: Rebuild and Reopen in Container'. VS Code should reopen your IDE inside the dev container, which should make you ready to start developing!

Tests should be available in the Testing tab. Debug tab also contains a flake8 and a runserver action.

Rebuild and Reopen in Container should create:

* A Django microservice on localhost:8000

* A HL7 FHIR API on localhost:8080

* Documentation on localhost:9000

Load FHIR synthetic data
-------------------------

Synthetic data of 1015 children (0 - 15 years-old) was generated with the Synthea patient generator. To load the data using the FHIR API, run the postSynthea.py script in a terminal outside the devcontainer environment:

::

    cd data/synthetic/synthea
    unzip fhir.zip
    python postSynthea.py

A mock Bundle was also generated to illustrate the ideal structure of FHIR resources for calculating indicators. This Bundle can be loaded using the HAPI FHIR Server interface > Server Actions > Transaction. Alternatively, a Bundle can also be loaded by doing a POST to the server base.
