from apps.users.models import User
from apps.ticketing.models import TheaterSeating, Show
from apps.reservations.models import Reservation


class SeatReservationMixin(object):
    def __init__(self, data, user):
        self.data = data
        self.user = user

    
    def run(self):
        self.__reserve_seat()
    
    def __reserve_seat(self):
        show_id = self.data.get("show")
        seats = self.data.get("seats")
        total_cost = self.data.get("total_cost")

        show = Show.objects.get(id=show_id)
        seat = TheaterSeating.objects.filter(id__in=seats)
  
        Reservation.objects.create(
            user=self.user,
            show=show,
            seat=seat,
            total_cost=total_cost
        )

        seat.booked = True
        seat.save()