from django.db import models
from apps.core.models import AbstractBaseModel


# Create your models here.
class Theater(AbstractBaseModel):
    name = models.CharField(max_length=255)
    location = models.JSONField(null=True)
    location_description = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    number_of_seats = models.IntegerField(default=1)
    number_of_rows = models.IntegerField(default=1)
    number_of_screens = models.IntegerField(default=1)
    opened_on = models.DateField(null=True)

    def __str__(self):
        return self.name


class TheaterSeat(AbstractBaseModel):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    booked = models.BooleanField(default=False)

    def __str__(self):
        return self.seat_number


class Seating(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    date = models.DateField()
    show_time = models.TimeField()


class Reservation(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    seating = models.ForeignKey(Seating, on_delete=models.CASCADE)
    seat_numbers = models.JSONField(default=list)
