from django.db import transaction
from apps.users.models import User
from apps.ticketing.models import TheaterSeating, Show
from apps.reservations.models import Reservation


class SeatReservationMixin(object):
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
        show_id = self.data.get("show")
        seats = self.data.get("seats")
        ticket_cost = self.data.get("ticket_cost")

        show = Show.objects.get(id=show_id)
        seat = TheaterSeating.objects.get(id=seats[0])

        Reservation.objects.create(
            user=self.user,
            show=show,
            seat=seat,
            ticket_cost=ticket_cost,
            reservation_type="Single Ticket",
        )

        seat.booked = True
        seat.save()

    @transaction.atomic
    def __reserve_multi_ticket(self):
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
        Reservation.objects.bulk_create(reservations)
        booked_seats.update(booked=True)
