from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.reservations.models import Reservation
from apps.users.models import User
from apps.ticketing.models import Theater, Show, TheaterSeating


class ReservationAPITestCase(APITestCase):
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

        self.dummy_reservations = Reservation.objects.bulk_create(
            [
                Reservation(
                    user=self.user,
                    show=self.show,
                    seat=self.seat,
                    ticket_cost=self.show.ticket_cost,
                    reservation_type="Single Ticket",
                    status="Active",
                    notification_send=False,
                ),
                Reservation(
                    user=self.user,
                    show=self.show,
                    seat=self.seat,
                    ticket_cost=self.show.ticket_cost,
                    reservation_type="Single Ticket",
                    status="Active",
                    notification_send=False,
                ),
                Reservation(
                    user=self.user,
                    show=self.show,
                    seat=self.seat,
                    ticket_cost=self.show.ticket_cost,
                    reservation_type="Single Ticket",
                    status="Active",
                    notification_send=False,
                ),
            ]
        )

        self.login_url = reverse("login")
        self.reservations_url = reverse("reservations")
        self.reserve_seat_url = reverse("reserve-seat")
        return super().setUp()

    def test_cannot_create_reservation_when_unauthenticated(self):
        data = {"seats": [269], "show": 6, "ticket_cost": 500}

        response = self.client.post(self.reserve_seat_url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_seat_can_be_reserved_when_authenticated(self):
        data = {
            "seats": [self.seat.id],
            "show": self.show.id,
            "ticket_cost": self.show.ticket_cost,
        }

        login_payload = {"username": self.user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.post(
            self.reserve_seat_url, data=data, headers=headers, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(Reservation.objects.count(), 1)
        self.assertIsInstance(response.json(), dict)

    def test_reservations_cannot_be_accessed_when_unauthenticated(self):
        response = self.client.get(self.reservations_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reservations_can_be_accessed_when_authenticated(self):
        login_payload = {"username": self.user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get(self.reservations_url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json()["results"], list)

    def test_reservation_can_be_fetched(self):
        reservation = Reservation.objects.first()

        login_payload = {"username": self.user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get(
            f"{self.reservations_url}{reservation.id}/", headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reservation_can_be_updated(self):
        reservation = Reservation.objects.first()

        login_payload = {"username": self.user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.patch(
            f"{self.reservations_url}{reservation.id}/",
            data={"status": "Cancelled"},
            headers=headers,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        fetch_response = self.client.get(
            f"{self.reservations_url}{reservation.id}/", headers=headers
        )
        self.assertEqual(fetch_response.status_code, 200)
        self.assertEqual(fetch_response.json()["status"], "Cancelled")

    def test_reservation_can_be_deleted(self):
        reservation = Reservation.objects.first()

        login_payload = {"username": self.user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.delete(
            f"{self.reservations_url}{reservation.id}/", headers=headers
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
