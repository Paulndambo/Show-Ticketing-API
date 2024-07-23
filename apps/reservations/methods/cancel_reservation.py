from django.db import transaction
from apps.ticketing.models import TheaterSeating
from apps.reservations.models import Reservation, MovieTicket
from apps.core.publisher import BasePublisher
from apps.notifications.tasks import ticket_cancellation_task


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
        self.__cancel_ticket_reservation()

 
    @transaction.atomic
    def __cancel_ticket_reservation(self):
        ticket = MovieTicket.objects.get(id=self.ticket_id)
        reservations = Reservation.objects.filter(ticket=ticket, user=self.user)
        reservations.update(status="Cancelled")

        seat_ids = list(reservations.values_list("seat_id", flat=True))
        seats = TheaterSeating.objects.filter(id__in=seat_ids)
        seats.update(booked=False)

        self.trigger_cancellation_notification(ticket=ticket)

    def trigger_cancellation_notification(self, ticket):
        ticket_cancellation_task.delay(ticket.id)
        """
        publisher = BasePublisher(
            routing_key="ticket_cancelled",
            body={
                "ticket_id": ticket.id
            }
        )
        publisher.run()
        """