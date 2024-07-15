from django.db import transaction
from apps.ticketing.models import Theater, TheaterSeat

class TheaterMixin:
    def __init__(self, data):
        self.data = data

    @transaction.atomic
    def onboard_theater(self):
        theater = self.__create_theater()
        self.__create_theater_seats(theater=theater)

    def __create_theater(self):
        theater = Theater.objects.create(**self.data)
        return theater

    def __create_theater_seats(self, theater):
        number_of_rows = theater.number_of_rows
        number_of_seats = theater.number_of_seats
        # Calculate the number of seats per row
        num_seats_per_row = number_of_seats // number_of_rows
        extra_seats = number_of_seats % number_of_rows
        
        seats = []
        seat_index = 1
        
        for row in range(1, number_of_rows + 1):
            row_letter = chr(64 + row)  # Convert row number to corresponding letter
            
            # Adjust number of seats in current row if extra seats are remaining
            seats_in_current_row = num_seats_per_row + (1 if extra_seats > 0 else 0)
            if extra_seats > 0:
                extra_seats -= 1
            
            for seat in range(1, seats_in_current_row + 1):
                seat_number = f"{row_letter}{seat}"
                seats.append(seat_number)
                seat_index += 1
        
        seat_instances = [TheaterSeat(theater=theater, seat_number=x) for x in seats]
        TheaterSeat.objects.bulk_create(seat_instances)