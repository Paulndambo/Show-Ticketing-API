from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User
from apps.ticketing.models import Theater

sample_data = {
    "name": "Juja Cinema",
    "location": {"lat": -1.2921, "lng": 36.8219},
    "location_description": "Next to JKUAT",
    "town": "Juja",
    "number_of_seats": 1,
    "number_of_screens": 1,
    "opened_on": "2024-01-01",
}


class TheaterAPIsTestCase(APITestCase):
    def setUp(self) -> None:
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

        self.theaters_url = reverse("theaters")
        self.login_url = reverse("login")
        return super().setUp()

    def test_customers_cannot_create_theaters(self):
        login_payload = {"username": self.customer_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.post(
            self.theaters_url, sample_data, headers=headers, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admins_can_create_theater(self):
        login_payload = {"username": self.admin_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.post(
            self.theaters_url, sample_data, headers=headers, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_theater_can_be_updated(self):
        theater = Theater.objects.create(**sample_data)
        theater.refresh_from_db()

        self.assertEqual(theater.name, "Juja Cinema")
        login_payload = {"username": self.admin_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        update_url = f"{self.theaters_url}{theater.id}/"
        data = {
            "name": "Juja Comrades Cinema",
            "location": {"lat": -1.2921, "lng": 36.8219},
            "location_description": "Next to JKUAT",
            "town": "Juja Town",
            "number_of_seats": 100,
            "number_of_screens": 4,
            "opened_on": "2024-01-01",
        }
        update_response = self.client.put(
            update_url, data=data, headers=headers, format="json"
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Theater.objects.get(id=theater.id).name, "Juja Comrades Cinema"
        )
        self.assertEqual(Theater.objects.get(id=theater.id).town, "Juja Town")
        self.assertEqual(Theater.objects.get(id=theater.id).number_of_seats, 100)
        self.assertEqual(Theater.objects.get(id=theater.id).number_of_screens, 4)

    def test_theater_can_be_patched(self):
        theater = Theater.objects.create(**sample_data)
        theater.refresh_from_db()

        self.assertEqual(theater.name, "Juja Cinema")
        login_payload = {"username": self.admin_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        patch_url = f"{self.theaters_url}{theater.id}/"
        data = {
            "name": "Juja Comrades Cinema and Conference",
            "location_description": "Next to JKUAT Gate C",
        }
        update_response = self.client.patch(
            patch_url, data=data, headers=headers, format="json"
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Theater.objects.get(id=theater.id).name,
            "Juja Comrades Cinema and Conference",
        )
        self.assertEqual(
            Theater.objects.get(id=theater.id).location_description,
            "Next to JKUAT Gate C",
        )

    def test_theater_can_be_deleted(self):
        theater = Theater.objects.create(**sample_data)
        theater.refresh_from_db()

        self.assertEqual(theater.name, "Juja Cinema")
        login_payload = {"username": self.admin_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        delete_url = f"{self.theaters_url}{theater.id}/"
        update_response = self.client.delete(delete_url, headers=headers, format="json")
        self.assertEqual(update_response.status_code, status.HTTP_204_NO_CONTENT)
