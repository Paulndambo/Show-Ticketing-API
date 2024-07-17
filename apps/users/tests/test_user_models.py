from django.test import TestCase
from apps.users.models import User


class CustomerUserModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="johndoe@gmail.com",
            phone_number="0712345678",
            gender="Male",
            role="Customer",
        )
        return super().setUp()

    def test_user_can_be_created(self):
        self.assertEqual(str(self.user), "John Doe")
        self.assertIsInstance(self.user, User)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.gender, "Male")
        self.assertEqual(self.user.role, "Customer")

    def test_customer_user_is_not_staff_user(self):
        self.assertNotEqual(self.user.is_staff, True)

    def test_customer_user_is_not_super_user(self):
        self.assertNotEqual(self.user.is_superuser, True)

    def test_customer_user_is_not_admin_user(self):
        self.assertNotEqual(self.user.role, "Admin")

    def test_user_can_be_updated(self):
        self.user.username = "jonniedoe"
        self.user.first_name = "Jonnie"
        self.user.last_name = "Doet"
        self.user.save()
        self.assertEqual(self.user.username, "jonniedoe")
        self.assertEqual(self.user.first_name, "Jonnie")
        self.assertEqual(self.user.last_name, "Doet")
        self.assertEqual(str(self.user), "Jonnie Doet")

    def test_user_can_be_deleted(self):
        self.user.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="johndoe")


class AdminUserModelTestCase(TestCase):
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
        return super().setUp()

    def test_admin_user_can_be_created(self):
        self.assertEqual(str(self.user), "Jane Doe")
        self.assertIsInstance(self.user, User)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.first_name, "Jane")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.gender, "Female")
        self.assertEqual(self.user.role, "Admin")

    def test_admin_user_is_staff_user(self):
        self.assertEqual(self.user.is_staff, True)

    def test_admin_user_is_super_user(self):
        self.assertEqual(self.user.is_superuser, True)

    def test_admin_user_is_not_customer_user(self):
        self.assertNotEqual(self.user.role, "Customer")

    def test_user_can_be_updated(self):
        self.user.username = "janiedoe"
        self.user.first_name = "Janie"
        self.user.last_name = "Doet"
        self.user.save()
        self.assertEqual(self.user.username, "janiedoe")
        self.assertEqual(self.user.first_name, "Janie")
        self.assertEqual(self.user.last_name, "Doet")
        self.assertEqual(str(self.user), "Janie Doet")

    def test_user_can_be_deleted(self):
        self.user.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="jandoe")
