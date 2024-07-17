from decimal import Decimal
from django.test import TestCase
from apps.ticketing.models import Theater, Show


class ShowTestCase(TestCase):
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
            ticket_cost=Decimal(500),
            show_date="2024-08-01",
            show_time="16:00",
        )
        return super().setUp()
    
    def test_show_can_created(self):
        self.assertEqual((str(self.show)), "FA Community Shield 2025")
        self.assertEqual(self.show.title, "FA Community Shield 2025")
        self.assertEqual(self.show.ticket_cost, 500)
        self.assertIsInstance(self.show.ticket_cost, Decimal)
        self.assertIsInstance(self.show.title, str)


    def test_show_can_be_updated(self):
        self.show.title = "EPL Community Shield 2025"
        self.show.ticket_cost = Decimal(1000)
        self.show.save()

        self.assertEqual(str(self.show), "EPL Community Shield 2025")
        self.assertEqual(self.show.title, "EPL Community Shield 2025")
        self.assertEqual(self.show.ticket_cost, 1000)
        self.assertIsInstance(self.show.title, str)
        self.assertIsInstance(self.show.ticket_cost, Decimal)
    
    def test_title_is_string(self):
        self.assertIsInstance(self.show.title, str)

    def test_show_can_be_deleted(self):
        self.show.delete()
        with self.assertRaises(Show.DoesNotExist):
            Show.objects.get(title="FA Community Shield 2025")