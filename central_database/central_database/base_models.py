import logging

from django.db import models

logger = logging.getLogger("logger")


class CDModel(models.Model):
    """
    Base abstract class for all CD Models. Changes here affect all models.
    """

    class Meta:
        abstract = True

    def __str__(self):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Alert(models.Model):
    """
    Base abstract class for all Alerts. Changes here affect all models.
    """

    class Meta:
        abstract = True

    def __str__(self):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
