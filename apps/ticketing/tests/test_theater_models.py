from datetime import date
from django.test import TestCase
from apps.ticketing.models import Theater

class ShowTestCase(TestCase):
    def setUp(self) -> None:
        self.theater = Theater.objects.create(
            name="Juja Cinema",
            location={"lat": -1.2921, "lng": 36.8219},
            location_description="Next to JKUAT",
            town="Juja",
            number_of_seats=1,
            number_of_screens=1,
            opened_on=date(2024, 7, 16),
        )
        return super().setUp()
    
    def test_theater_creation(self):
        self.assertEqual(self.theater.town, "Juja")
        self.assertEqual(self.theater.name, "Juja Cinema")
        self.assertEqual(self.theater.town, "Juja")
        self.assertEqual(self.theater.location_description, "Next to JKUAT")
        self.assertEqual(self.theater.location, {"lat": -1.2921, "lng": 36.8219})
        self.assertEqual(str(self.theater.opened_on), "2024-07-16")
        self.assertEqual(self.theater.number_of_screens, 1)
        self.assertEqual(self.theater.number_of_seats, 1)

    def test_theater_belongs_to_theater_class(self):
        self.assertIsInstance(self.theater, Theater)

    def test_name_is_string(self):
        self.assertIsInstance(self.theater.name, str)

    def test_town_is_string(self):
        self.assertIsInstance(self.theater.town, str)

    def test_location_description_is_string(self):
        self.assertIsInstance(self.theater.location_description, str)
    
    def test_number_of_seats_is_integer(self):
        self.assertIsInstance(self.theater.number_of_seats, int)
    
    def test_number_of_screens_is_integer(self):
        self.assertIsInstance(self.theater.number_of_screens, int)

    def test_opened_on_is_date(self):
        self.assertIsInstance(self.theater.opened_on, date)

    def test_location_is_dict(self):
        self.assertIsInstance(self.theater.location, dict)
        

    def test_theater_can_be_updated(self):
        self.theater.name = "Juja Comrades Cinema"
        self.theater.number_of_seats = 100
        self.theater.number_of_screens = 5
        self.theater.save()

        self.assertEqual(str(self.theater), "Juja Comrades Cinema")
        self.assertEqual(self.theater.number_of_screens, 5)
        self.assertEqual(self.theater.number_of_seats, 100)
        updated_theater = Theater.objects.get(id=self.theater.id)
        self.assertEqual(updated_theater.name, "Juja Comrades Cinema")

    def test_theater_with_null_location(self):
        theater = Theater.objects.create(
            name="Theater with null location",
            location_description="Unknown location",
            town="Unknown",
            number_of_seats=100,
            number_of_screens=1,
            opened_on="2023-01-01"
        )
        self.assertIsNone(theater.location)
        self.assertEqual(theater.location_description, "Unknown location")

    def test_theater_with_default_number_of_screens(self):
        theater = Theater.objects.create(
            name="Theater with default screens",
            location={"lat": -1.2921, "lng": 36.8219},
            location_description="Nairobi CBD",
            town="Nairobi",
            number_of_seats=150,
            opened_on="2023-06-01"
        )
        self.assertEqual(theater.number_of_screens, 1)

    def test_theater_without_opened_on_date(self):
        theater = Theater.objects.create(
            name="Theater without opened_on",
            location={"lat": -1.2921, "lng": 36.8219},
            location_description="Nairobi CBD",
            town="Nairobi",
            number_of_seats=200,
            number_of_screens=3
        )
        self.assertIsNone(theater.opened_on)

    def test_theater_can_be_deleted(self):
        self.theater.delete()
        with self.assertRaises(Theater.DoesNotExist):
            Theater.objects.get(name="Juja Cinema")