from django.test import TestCase
from apps.ticketing.models import TheaterSeating, Theater, Show

class TheaterSeatingTestCase(TestCase):
    def setUp(self) -> None:
        self.theater = Theater.objects.create(
            name="Juja Cinema",
            location=[1.234, 36.789],
            location_description="Next to JKUAT",
            town="Juja",
            number_of_seats=1,
            number_of_screens=1,
            opened_on="2024-07-16",
        )

        self.show = Show.objects.create(
            title="FA Community Shield 2025",
            theater=self.theater,
            ticket_cost=500,
            show_date="2024-08-01",
            show_time="16:00",
        )
        self.seat = TheaterSeating.objects.create(
            theater=self.theater,
            show=self.show,
            seat_number="A1",
            booked=False,
            seating_date="2024-08-01",
        )
        return super().setUp()
    
    def test_seating_can_be_created(self):
        self.assertEqual(str(self.seat), "A1")
        self.assertEqual(self.seat.booked, False)
        self.assertIsInstance(self.seat.show, Show)
        self.assertEqual(str(self.seat.show), "FA Community Shield 2025")
        self.assertIsInstance(self.seat.theater, Theater)
        self.assertEqual(str(self.seat.theater), "Juja Cinema")

    def test_seating_can_be_updated(self):
        self.seat.seat_number = "A0"
        self.seat.booked = True
        self.seat.save()

        self.assertEqual(str(self.seat), "A0")
        self.assertEqual(self.seat.booked, True)

    def test_seating_can_be_deleted(self):
        self.seat.delete()
        with self.assertRaises(TheaterSeating.DoesNotExist):
            TheaterSeating.objects.get(seat_number="A1")

