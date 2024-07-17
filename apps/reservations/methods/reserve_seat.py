from django.db import transaction
from apps.users.models import User
from apps.ticketing.models import TheaterSeating, Show
from apps.reservations.models import Reservation

from apps.notifications.tasks import seat_reservation_task


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

        reservation = Reservation.objects.create(
            user=self.user,
            show=show,
            seat=seat,
            ticket_cost=ticket_cost,
            reservation_type="Single Ticket",
        )

        seat.booked = True
        seat.save()

        seat_reservation_task.delay(self.user.id, show.id, [reservation.id])


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

        reservations = [
            Reservation(
                user=self.user,
                show=show,
                seat=seat,
                ticket_cost=ticket_cost,
                reservation_type="Multi Ticket",
            )
            for seat in booked_seats
        ]
        reservations_list = Reservation.objects.bulk_create(reservations)
        booked_seats.update(booked=True)

        reservations_ids = [x.id for x in reservations_list]
        seat_reservation_task.delay(self.user.id, show.id, reservations_ids)
