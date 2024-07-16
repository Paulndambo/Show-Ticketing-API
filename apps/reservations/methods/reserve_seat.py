from apps.users.models import User
from apps.ticketing.models import TheaterSeating, Show
from apps.reservations.models import Reservation


class SeatReservationMixin(object):
    def __init__(self, data):
        self.data = data

    
    def run(self):
        self.__reserve_seat()
    
    def __reserve_seat(self):
        user_id = self.data.get("customer")
        show_id = self.data.get("show")
        seat_id = self.data.get("seat")
        total_cost = self.data.get("total_cost")

        user = User.objects.get(id=user_id)
        show = Show.objects.get(id=show_id)
        seat = TheaterSeating.objects.get(id=seat_id)

        if seat.booked:
            raise ValueError("This seat has already been booked")
        
        Reservation.objects.create(
            user=user,
            show=show,
            seat=seat,
            total_cost=total_cost
        )

        seat.booked = True
        seat.save()
        
