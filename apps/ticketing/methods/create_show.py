from django.db import transaction
from apps.ticketing.models import Show, TheaterSeating


class CreateShowMixin(object):
    """
    This class contains all the logic need to create a new show.

    args:
        - data: payload to create a show.

    returns:
         - None.
    """

    def __init__(self, data):
        self.data = data

    @transaction.atomic
    def run(self):
        show = self.__create_show()
        self.__generate_seating_arrangement(show=show)

    def __create_show(self):
        show = Show.objects.create(
            title=self.data.get("title"),
            theater_id=self.data.get("theater"),
            ticket_cost=self.data.get("ticket_cost"),
            show_date=self.data.get("show_date"),
            show_time=self.data.get("show_time"),
        )
        return show

    def __generate_seating_arrangement(self, show):
        """
        This method is used to generate the seating arrangement for a certain show in a certain theater.

        args:
            - show: The show for which the arrangement is need.

        returns:
            - None
        """
        try:
            number_of_rows = self.data.get("seating_arrangement").get("number_of_rows", 0)
            
            number_of_seats = show.theater.number_of_seats

            # Calculate the number of seats per row
            num_seats_per_row = number_of_seats // number_of_rows
            extra_seats = number_of_seats % number_of_rows

            num_seats_per_row = number_of_seats // number_of_rows
            extra_seats = number_of_seats % number_of_rows

            seats = []

            for row in range(1, number_of_rows + 1):
                row_letter = chr(
                    64 + row
                )  # Converting row number to corresponding letter

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
                    theater=show.theater,
                    show=show,
                    seating_date=show.show_date,
                    seat_number=x,
                )
                for x in seats
            ]
            TheaterSeating.objects.bulk_create(seat_instances)
        except Exception as e:
            raise e
