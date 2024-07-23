from django.db import transaction
from apps.ticketing.models import TheaterSeating, Show
from apps.reservations.models import Reservation, MovieTicket

class SeatReservationMixin(object):
    """
    This class deals with seat reservation

    args:
        - data: payload to reserve a seat.
        - user: the person reserving a seat.

    returns:
        - None
    """

    def __init__(self, data, user):
        self.data = data
        self.user = user

    def run(self):
        if len(self.data["seats"]) >= 2:
            self.__reserve_multi_ticket()
        else:
            self.__reserve_single_seat()

    @transaction.atomic
    def __reserve_single_seat(self):
        """
        This method is invoked when a customer is reserving one seat
        """
        show_id = self.data.get("show")
        seats = self.data.get("seats")
        ticket_cost = self.data.get("ticket_cost")

        show = Show.objects.get(id=show_id)
        seat = TheaterSeating.objects.get(id=seats[0])

        ticket = MovieTicket.objects.create(
            user=self.user,
            ticket_cost=ticket_cost,
            show=show,
            reservation_type="Single Ticket",
            notification_send=False,
        )

        Reservation.objects.create(
            ticket=ticket,
            user=self.user,
            show=show,
            seat=seat,
            ticket_cost=ticket_cost,
            reservation_type="Single Ticket",
        )

        seat.booked = True
        seat.save()

        self.trigger_reservation_notification(ticket=ticket)

    @transaction.atomic
    def __reserve_multi_ticket(self):
        """
        This function is invoked when a customer is reserving more than one seats
        """
        show_id = self.data.get("show")
        seats = self.data.get("seats")
        ticket_cost = self.data.get("ticket_cost")

        show = Show.objects.get(id=show_id)
        booked_seats = TheaterSeating.objects.filter(id__in=seats)

        ticket = MovieTicket.objects.create(
            user=self.user,
            ticket_cost=ticket_cost,
            show=show,
            reservation_type="Multi Ticket",
            notification_send=False,
        )

        reservations = [
            Reservation(
                ticket=ticket,
                user=self.user,
                show=show,
                seat=seat,
                ticket_cost=ticket_cost,
                reservation_type="Multi Ticket",
            )
            for seat in booked_seats
        ]
        Reservation.objects.bulk_create(reservations)
        booked_seats.update(booked=True)

        self.trigger_reservation_notification(ticket=ticket)

    def trigger_reservation_notification(self, ticket):
        #seat_reservation_task(ticket.id)
        pass
