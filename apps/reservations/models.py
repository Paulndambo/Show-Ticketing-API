from django.db import models
from apps.core.models import AbstractBaseModel
from apps.core.constants import RESERVATION_TYPES


# Create your models here.
class Reservation(AbstractBaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    show = models.ForeignKey("ticketing.Show", on_delete=models.PROTECT)
    seat = models.OneToOneField("ticketing.TheaterSeating", on_delete=models.PROTECT)
    ticket_cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    reservation_type = models.CharField(
        max_length=255, choices=RESERVATION_TYPES, null=True
    )
