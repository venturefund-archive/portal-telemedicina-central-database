Testing
=======

The Child Health Tracker uses Django's built-in testing framework along with pytest for unit and integration tests.

Running Tests
-------------

To run the test suite:

.. code-block:: bash

   python manage.py test

Or with pytest:

.. code-block:: bash

   pytest

Writing Tests
-------------

When writing new features or fixing bugs, make sure to add appropriate tests. Place your tests in the `tests` directory of each Django app.

Example test:

.. code-block:: python

   from django.test import TestCase
   from .models import Child

   class ChildModelTest(TestCase):
       def test_string_representation(self):
           child = Child(name="Test Child")
           self.assertEqual(str(child), child.name)
