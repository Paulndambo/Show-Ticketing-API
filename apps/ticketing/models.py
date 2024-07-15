from django.db import models
from apps.core.models import AbstractBaseModel
# Create your models here.
class Theatre(AbstractBaseModel):
    name = models.CharField(max_length=255)
    location = models.JSONField(null=True)
    location_description = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    number_of_seats = models.IntegerField(default=1)
    number_of_screens = models.IntegerField(default=1)
    opened_on = models.DateField(null=True)

    def __str__(self):
        return self.name
