from django.test import TestCase
from apps.reservations.models import Reservation
from apps.users.models import User
from apps.ticketing.models import Theater, Show, TheaterSeating


class ReservationTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            first_name="Jane",
            last_name="Doe",
            username="janedoe",
            email="janedoe@gmail.com",
            phone_number="0712345678",
            gender="Female",
            role="Admin",
            is_staff=True,
            is_superuser=True,
        )
        self.user.set_password("1234")
        self.user.save()

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
        self.reservation = Reservation.objects.create(
            user=self.user,
            show=self.show,
            seat=self.seat,
            ticket_cost=self.show.ticket_cost,
            reservation_type="Single Ticket",
            status="Active",
            notification_send=False,
        )
        self.reservation.seat.booked = True
        self.reservation.seat.save()

        return super().setUp()

    def test_reservation_can_be_created(self):
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(self.reservation.status, "Active")
        self.assertNotEqual(self.reservation.notification_send, True)
        self.assertNotEqual(self.reservation.reservation_type, "Multi Ticket")

    def test_reservation_can_be_cancelled(self):
        self.reservation.status = "Cancelled"
        self.reservation.save()

        self.reservation.seat.booked = False
        self.reservation.seat.save()

        self.assertEqual(self.reservation.status, "Cancelled")
        self.assertEqual(self.reservation.seat.booked, False)

    def test_reservation_can_be_reset(self):
        self.reservation.status = "Active"
        self.reservation.save()

        self.reservation.seat.booked = True
        self.reservation.seat.save()

        self.assertEqual(self.reservation.status, "Active")
        self.assertEqual(self.reservation.seat.booked, True)

    def test_reservation_cost_equals_show_ticket_cost(self):
        self.assertEqual(
            self.reservation.ticket_cost, self.reservation.show.ticket_cost
        )

    def test_reservation_notification_is_not_send_by_default(self):
        self.assertEqual(self.reservation.notification_send, False)

    def test_reservation_can_be_deleted(self):
        self.reservation.delete()
        with self.assertRaises(Reservation.DoesNotExist):
            Reservation.objects.get(id=self.reservation.id)
