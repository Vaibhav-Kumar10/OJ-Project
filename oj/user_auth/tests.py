from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class AuthTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password123"
        )

    def test_login_valid(self):
        response = self.client.post(
            reverse("user_auth:login"), {"uname": "testuser", "password": "password123"}
        )
        self.assertRedirects(response, reverse("core:home"))

    def test_login_invalid(self):
        response = self.client.post(
            reverse("user_auth:login"), {"uname": "wrong", "password": "wrong"}
        )
        self.assertContains(response, "Invalid username or password")

    def test_signup(self):
        response = self.client.post(
            reverse("user_auth:signup"),
            {
                "fname": "John",
                "lname": "Doe",
                "uname": "newuser",
                "email": "j@x.com",
                "mobileno": "1234567890",
                "password": "abc123",
                "repassword": "abc123",
            },
        )
        self.assertRedirects(response, reverse("core:home"))
