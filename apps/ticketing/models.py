from django.db import models
from apps.core.models import AbstractBaseModel


# Create your models here.
class Theater(AbstractBaseModel):
    name = models.CharField(max_length=255)
    location = models.JSONField(null=True)
    location_description = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    number_of_seats = models.IntegerField()
    number_of_screens = models.IntegerField(default=1)
    opened_on = models.DateField(null=True)

    def __str__(self):
        return self.name


class Show(models.Model):
    title = models.CharField(max_length=255)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    ticket_cost = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateField()
    show_time = models.TimeField()

    def __str__(self):
        return self.title


class TheaterSeating(AbstractBaseModel):
    theater = models.ForeignKey(Theater, on_delete=models.PROTECT)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    booked = models.BooleanField(default=False)
    seating_date = models.DateField(null=True)

    def __str__(self):
        return self.seat_number

