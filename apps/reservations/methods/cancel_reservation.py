from django.db import transaction
from apps.ticketing.models import TheaterSeating
from apps.reservations.models import Reservation, MovieTicket


class CancelReservationMixin(object):
    """
    This class deals with all the logic around cancelling a reservation.

    args:
        - data: payload containing reservations to cancel.
        - user: the owner of the reservation.

    returns:
        - None.
    """

    def __init__(self, ticket_id, user):
        self.ticket_id = ticket_id
        self.user = user

    def run(self):
        if len(self.data.get("seats")) >= 2:
            self.__cancel_multi_seat_reservation()

        self.__cancel_single_seat_reservation()

    @transaction.atomic
    def __cancel_single_seat_reservation(self):
        ticket = MovieTicket.objects.get(id=self.ticket_id)
        reservation = Reservation.objects.get(ticket=ticket, user=self.user)
        reservation.status = "Cancelled"
        reservation.save()

        reservation.seat.booked = False
        reservation.seat.save()

        self.trigger_cancellation_notification(ticket=ticket)

    @transaction.atomic
    def __cancel_multi_seat_reservation(self):
        ticket = MovieTicket.objects.get(id=self.ticket_id)
        reservations = Reservation.objects.filter(ticket=ticket, user=self.user)
        reservations.update(status="Cancelled")

        seat_ids = list(reservations.values_list("seat_id", flat=True))
        seats = TheaterSeating.objects.filter(id__in=seat_ids)
        seats.update(booked=False)

        self.trigger_cancellation_notification(ticket=ticket)

    def trigger_cancellation_notification(self, ticket):
        #ticket_cancellation_task.delay(ticket.id)
        pass
