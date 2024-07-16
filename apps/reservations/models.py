from django.db import models
from apps.core.models import AbstractBaseModel
from apps.core.constants import RESERVATION_TYPES, RESERVATION_STATUS


# Create your models here.
class Reservation(AbstractBaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="customerreservations")
    show = models.ForeignKey("ticketing.Show", on_delete=models.PROTECT, related_name="showreservations")
    seat = models.ForeignKey("ticketing.TheaterSeating", on_delete=models.PROTECT)
    ticket_cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    reservation_type = models.CharField(
        max_length=255, choices=RESERVATION_TYPES, null=True
    )
    status = models.CharField(max_length=255, choices=RESERVATION_STATUS, default="Active")
    notification_send = models.BooleanField(default=False)
