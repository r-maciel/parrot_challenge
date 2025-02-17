from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from api.models.waiter import Waiter


class TestWaiterView(TestCase):
    """ Test cases for the WaiterDetailView """

    def setUp(self):
        """Set up test client and sample users."""
        self.client = APIClient()

        self.superuser = get_user_model().objects.create_superuser(
            email="admin@example.com", name="Admin", password="securepassword"
        )
        self.regular_user = get_user_model().objects.create_user(
            email="user@example.com", name="User", password="securepassword"
        )

        self.valid_payload = {
            "email": "waiter@example.com",
            "name": "Pedro",
            "password": "securepassword"
        }

    def test_superuser_can_create_waiter(self):
        """ SuperUser can create a Waiter """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post("/api/waiters/", self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], self.valid_payload["email"])
        self.assertEqual(response.data["name"], self.valid_payload["name"])
        self.assertEqual(
            Waiter.objects.filter(email="waiter@example.com").count(), 1
        )

    def test_non_superuser_cannot_create_waiter(self):
        """ Non-SuperUser can't create a waiter receives 403 Forbidden """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post("/api/waiters/", self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_create_waiter(self):
        """ Unauthenticated user receives 401 Unauthorized """
        response = self.client.post("/api/waiters/", self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_data_fails_validation(self):
        """ Invalid data results dails validation """
        self.client.force_authenticate(user=self.superuser)
        invalid_payload = {
            "email": "invalid-email",
            "name": "",
            "password": ""
        }
        response = self.client.post("/api/waiters/", invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
