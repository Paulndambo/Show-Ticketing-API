from django.db import models
from apps.core.models import AbstractBaseModel
from apps.core.constants import RESERVATION_TYPES, RESERVATION_STATUS


# Create your models here.
class MovieTicket(AbstractBaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    ticket_cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    show = models.ForeignKey(
        "ticketing.Show",
        on_delete=models.SET_NULL,
        null=True,
        related_name="showtickets",
    )
    status = models.CharField(
        max_length=255, choices=RESERVATION_STATUS, default="Active"
    )
    reservation_type = models.CharField(
        max_length=255, choices=RESERVATION_TYPES, null=True
    )
    notification_send = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name


class Reservation(AbstractBaseModel):
    ticket = models.ForeignKey(
        MovieTicket,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ticketreservations",
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="customerreservations"
    )
    show = models.ForeignKey(
        "ticketing.Show", on_delete=models.PROTECT, related_name="showreservations"
    )
    seat = models.ForeignKey("ticketing.TheaterSeating", on_delete=models.PROTECT)
    ticket_cost = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    reservation_type = models.CharField(
        max_length=255, choices=RESERVATION_TYPES, null=True
    )
    status = models.CharField(
        max_length=255, choices=RESERVATION_STATUS, default="Active"
    )
    notification_send = models.BooleanField(default=False)

    def __str__(self):
        return self.seat.seat_number
