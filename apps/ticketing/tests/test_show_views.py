from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User
from apps.ticketing.models import Show, Theater

class ShowAPIsTestCase(APITestCase):
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

        self.login_url = reverse("login")
        self.shows_url = reverse("shows")
        return super().setUp()
    
    def test_customers_cannot_create_shows(self):
        login_payload = {"username": self.customer_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.post(self.shows_url, self.sample_data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admins_can_create_shows(self):
        login_payload = {"username": self.admin_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.post(self.shows_url, self.sample_data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_users_can_fetch_shows(self):
        response = self.client.get(self.shows_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json()["results"], list)

    def test_show_can_be_updated(self):
        self.sample_data.pop("seating_arrangement")
        self.sample_data["theater"] = self.theater
        show = Show.objects.create(**self.sample_data)
        show.refresh_from_db()

        self.assertEqual(show.title, "FA Community Shield 2025")
        login_payload = {"username": self.admin_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        update_url = f"{self.shows_url}{show.id}/"
        data = {
            "title": "EPL Community Shield 2025",
            "theater": self.theater.id,
            "ticket_cost": 1500,
            "show_date": "2024-08-01",
            "show_time": "16:00",
            "seating_arrangement": {
                "number_of_rows": 7
            }
        }
        update_response = self.client.put(update_url, data=data, headers=headers, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Show.objects.get(id=show.id).title, "EPL Community Shield 2025")
        self.assertEqual(Show.objects.get(id=show.id).ticket_cost, 1500)
        self.assertEqual(str(Show.objects.get(id=show.id).show_date), "2024-08-01")
        self.assertEqual(str(Show.objects.get(id=show.id).show_time), "16:00:00")

    def test_show_can_be_patched(self):
        self.sample_data.pop("seating_arrangement")
        self.sample_data["theater"] = self.theater
        show = Show.objects.create(**self.sample_data)
        show.refresh_from_db()

        self.assertEqual(show.title, "FA Community Shield 2025")
        login_payload = {"username": self.admin_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        patch_url = f"{self.shows_url}{show.id}/"
        data = {"title": "EPL Community Shield 2025", "ticket_cost": 1000}
        update_response = self.client.patch(patch_url, data=data, headers=headers, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Show.objects.get(id=show.id).title, "EPL Community Shield 2025")
        self.assertEqual(Show.objects.get(id=show.id).ticket_cost, 1000)

    def test_show_can_be_deleted(self):
        self.sample_data.pop("seating_arrangement")
        self.sample_data["theater"] = self.theater
        show = Show.objects.create(**self.sample_data)
        show.refresh_from_db()

        self.assertEqual(show.title, "FA Community Shield 2025")
        login_payload = {"username": self.admin_user.username, "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        delete_url = f"{self.shows_url}{show.id}/"
        update_response = self.client.delete(delete_url, headers=headers, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_204_NO_CONTENT)