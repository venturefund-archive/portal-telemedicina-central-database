Backend Documentation
=====================

.. toctree::
   :maxdepth: 2

   models
   views
   serializers
   urls

Architecture Overview
---------------------

The Child Health Tracker backend is built using Django and Django Rest Framework. It follows a typical Django project structure with the following main components:

- Models: Define the database schema and relationships
- Views: Handle the business logic and request processing
- Serializers: Convert complex data types to Python datatypes that can then be easily rendered into JSON
- URLs: Define the routing for the API endpoints

Key Technologies
----------------

- Django 3.2.14
- Django Rest Framework 3.13.1
- PostgreSQL (database)
- Redis (caching and message broker)
- Channels (for WebSocket support)

For a complete list of dependencies, refer to the `requirements.txt` file in the project root.
