Database Models
===============

This section describes the main database models used in the Child Health Tracker.

.. toctree::
   :maxdepth: 2

   child
   growth_record
   vaccination
   milestone

Child
-----

.. code-block:: python

   class Child(models.Model):
       name = models.CharField(max_length=100)
       date_of_birth = models.DateField()
       gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
       parent = models.ForeignKey(User, on_delete=models.CASCADE)

       def __str__(self):
           return self.name

(Continue with other models)
