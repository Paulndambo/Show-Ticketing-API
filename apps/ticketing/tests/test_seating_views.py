from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User
from apps.ticketing.models import Show, Theater, TheaterSeating

class SeatingArrangementAPIsTestCase(APITestCase):
    def setUp(self) -> None:
        self.theater = Theater.objects.create(
            name="Juja Cinema",
            location=[1.234, 36.789],
            location_description="Next to JKUAT",
            town="Juja",
            number_of_seats=100,
            number_of_screens=5,
            opened_on="2024-07-16",
        )

        self.show = Show.objects.create(
            title="FA Community Shield 2025",
            theater=self.theater,
            ticket_cost=500,
            show_date="2024-08-01",
            show_time="16:00",
        )
        self.sample_data = {
            "title": "FA Community Shield 2025",
            "theater": self.theater.id,
            "ticket_cost": 500,
            "show_date": "2024-08-01",
            "show_time": "16:00",
            "seating_arrangement": {
                "number_of_rows": 7
            }
        }
        self.customer_user = User.objects.create(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="johndoe@gmail.com",
            phone_number="0712345678",
            gender="Male",
            role="Customer",
        )
        self.customer_user.set_password("1234")
        self.customer_user.save()

        self.admin_user = User.objects.create(
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
        self.admin_user.set_password("1234")
        self.admin_user.save()
        self.login_url = reverse("login")
        self.shows_url = reverse("shows")
        self.seatings_url = reverse("seatings")
        return super().setUp()
    
    def test_customers_cannot_create_seating_arrangements(self):
        login_payload = {"username": self.customer_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.post(self.shows_url, self.sample_data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customers_can_fetch_seating_arrangements(self):
        login_payload = {"username": self.customer_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get(self.seatings_url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json()["results"], list)

    def test_seating_arrangements_can_be_fetched_when_unauthenticated(self):
        response = self.client.get(self.seatings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json()["results"], list)

    def test_admins_can_create_seating_arrangements(self):
        login_payload = {"username": self.admin_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.post(self.shows_url, self.sample_data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        fetch_response = self.client.get(self.seatings_url, headers=headers)
        self.assertEqual(fetch_response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(fetch_response.json()["results"], list)
        self.assertEqual(len(fetch_response.json()["results"]), 10) # Show he 100 but because of pagination you get 10

    def test_customer_cannot_edit_seating(self):
        seating = TheaterSeating.objects.create(
            theater=self.theater,
            show=self.show,
            seat_number="Q9"
        )
        seating.refresh_from_db()

        editing_data = {
            "seat_number": "Q6"
        }
        login_payload = {"username": self.customer_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.patch(f"{self.seatings_url}{seating.id}/", data=editing_data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_admin_can_edit_seating(self):
        seating = TheaterSeating.objects.create(
            theater=self.theater,
            show=self.show,
            seat_number="Q9"
        )
        seating.refresh_from_db()

        editing_data = {
            "seat_number": "Q6"
        }
        login_payload = {"username": self.admin_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.patch(f"{self.seatings_url}{seating.id}/", data=editing_data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_cannot_delete_seating(self):
        seating = TheaterSeating.objects.create(
            theater=self.theater,
            show=self.show,
            seat_number="Q9"
        )
        seating.refresh_from_db()


        login_payload = {"username": self.customer_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.delete(f"{self.seatings_url}{seating.id}/",headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_seating(self):
        seating = TheaterSeating.objects.create(
            theater=self.theater,
            show=self.show,
            seat_number="Q9"
        )
        seating.refresh_from_db()


        login_payload = {"username": self.admin_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.delete(f"{self.seatings_url}{seating.id}/",headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
