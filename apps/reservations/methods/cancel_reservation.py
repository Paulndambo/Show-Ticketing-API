from django.db import transaction
from apps.users.models import User
from apps.ticketing.models import TheaterSeating, Show
from apps.reservations.models import Reservation


class CancelReservationMixin(object):
    """
    This class deals with all the logic around cancelling a reservation.

    args:
        - data: payload containing reservations to cancel.
        - user: the owner of the reservation.

    returns:
        - None.
    """
    def __init__(self, data, user):
        self.data = data
        self.user = user

    def run(self):
        if len(self.data.get("seats")) >= 2:
            self.__cancel_multi_seat_reservation()

        self.__cancel_single_seat_reservation()

    @transaction.atomic
    def __cancel_single_seat_reservation(self):
        reservation = Reservation.objects.get(id=self.data["seats"][0], user=self.user)
        reservation.status = "Cancelled"
        reservation.save()

        reservation.seat.booked = False
        reservation.seat.save()

    @transaction.atomic
    def __cancel_multi_seat_reservation(self):
        reservations = Reservation.objects.filter(id__in=self.data["seats"])
        reservations.update(status="Cancelled")

        seat_ids = list(reservations.values_list("seat_id", flat=True))
        seats = TheaterSeating.objects.filter(id__in=seat_ids)
        seats.update(booked=False)
