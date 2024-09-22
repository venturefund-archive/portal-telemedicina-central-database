API Documentation
=================

This section provides details about the available API endpoints in the Child Health Tracker.

.. toctree::
   :maxdepth: 2

   authentication
   children
   growth
   vaccinations
   milestones

Authentication
--------------

All API endpoints, except for authentication-related ones, require a valid JWT token. Include the token in the Authorization header of your requests:

.. code-block:: http

   Authorization: Bearer <your_token_here>

Endpoints
---------

Children
~~~~~~~~

- GET /api/children/: List all children
- POST /api/children/: Create a new child
- GET /api/children/{id}/: Retrieve a specific child
- PUT /api/children/{id}/: Update a child
- DELETE /api/children/{id}/: Delete a child

(Continue with other endpoint groups)
