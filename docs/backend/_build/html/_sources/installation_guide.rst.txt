How to create a development environment
=======================================

Pre-requisites
--------------

- Visual Studio Code editor
- Docker for your operating system
- Git

Clone repository
----------------

1. Open a terminal or command prompt
2. Run the following command:

   .. code-block:: bash

      git clone https://github.com/your-repo/child-health-tracker.git
      cd child-health-tracker

Remote Container
----------------

To use the development IDE:

1. Open the project folder with VS Code
2. Press 'F1'
3. Search for: 'Remote-Containers: Rebuild and Reopen in Container'
4. VS Code should reopen your IDE inside the dev container

This will set up your development environment with all necessary dependencies.

Database Setup
--------------

1. The development container includes a PostgreSQL database. To set it up:

   .. code-block:: bash

      python manage.py migrate

2. Create a superuser:

   .. code-block:: bash

      python manage.py createsuperuser

Running the Development Server
------------------------------

To start the development server:

.. code-block:: bash

   python manage.py runserver 0.0.0.0:8000

The API will be available at `http://localhost:8000/api/`.

Load FHIR synthetic data
------------------------

(Include instructions for loading FHIR synthetic data here)
