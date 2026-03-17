from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser", email="test@test.com", password="12345678"
        )
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("12345678"))

    def test_str(self):
        user = User.objects.create_user(
            username="user2", email="user2@test.com", password="12345678"
        )
        self.assertEqual(str(user), user.username)
