from django.db import transaction
from apps.ticketing.models import Theater, Show, TheaterSeating


class SeatingArrangementGenerator:
    def __init__(self, data):
        self.data = data

    @transaction.atomic
    def generate_seating_arrangement(self):
        theater_id = self.data.get("theater")
        show_id = self.data.get("show")

        theater = Theater.objects.get(id=theater_id)
        show = Show.objects.get(id=show_id)

        number_of_rows = self.data.get("number_of_rows")
        number_of_seats = theater.number_of_seats

        # Calculate the number of seats per row
        num_seats_per_row = number_of_seats // number_of_rows
        extra_seats = number_of_seats % number_of_rows

        num_seats_per_row = number_of_seats // number_of_rows
        extra_seats = number_of_seats % number_of_rows

        seats = []

        for row in range(1, number_of_rows + 1):
            row_letter = chr(64 + row)  # Convert row number to corresponding letter

            # Determine the number of seats in the current row
            if row == number_of_rows:
                seats_in_current_row = num_seats_per_row + extra_seats
            else:
                seats_in_current_row = num_seats_per_row

            for seat in range(1, seats_in_current_row + 1):
                seat_number = f"{row_letter}{seat}"
                seats.append(seat_number)

        seat_instances = [
            TheaterSeating(
                theater=theater, show=show, seating_date=show.date, seat_number=x
            )
            for x in seats
        ]
        TheaterSeating.objects.bulk_create(seat_instances)
