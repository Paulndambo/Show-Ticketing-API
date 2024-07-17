from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User


class UserAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.user_list_url = reverse("users")
        return super().setUp()

    def test_user_can_register(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@gmail.com",
            "phone_number": "0712345678",
            "gender": "Male",
            "role": "Customer",
            "password": "1234",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().first_name, "John")

    def test_user_can_login(self):
        user = User.objects.create(
            first_name="Jane",
            last_name="Doe",
            username="janedoe",
            email="janedoe@gmail.com",
            phone_number="0712345678",
            gender="Female",
            role="Customer",
        )
        user.set_password("1234")
        user.save()

        login_payload = {"username": "janedoe", "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), dict)

    def test_customer_user_can_only_see_their_profile(self):
        user = User.objects.create(
            first_name="Jane",
            last_name="Doe",
            username="janedoe",
            email="janedoe@gmail.com",
            phone_number="0712345678",
            gender="Female",
            role="Customer",
            is_staff=False,
            is_superuser=False,
        )
        user.set_password("1234")
        user.save()

        login_payload = {"username": "janedoe", "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        users_response = self.client.get(self.user_list_url, headers=headers)
        self.assertEqual(users_response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(users_response.json()["results"][0], dict)

    def test_only_admin_can_see_all_users(self):
        user = User.objects.create(
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
        user.set_password("1234")
        user.save()

        login_payload = {"username": "janedoe", "password": "1234"}
        response = self.client.post(self.login_url, login_payload, format="json")
        token = response.json()["access"]

        headers = {"Authorization": f"Bearer {token}"}

        users_response = self.client.get(self.user_list_url, headers=headers)
        self.assertEqual(users_response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(users_response.json()["results"], list)

    def test_users_cannot_be_accessed_when_unauthenticated(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
