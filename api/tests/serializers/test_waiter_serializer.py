from django.test import TestCase
from api.models.waiter import Waiter
from api.serializers.waiter_serializer import WaiterSerializer


class WaiterSerializerTest(TestCase):
    """Test cases for the WaiterSerializer"""

    def test_creates_waiter_succesfully(self):
        """ Create waiter successfully """
        data = {
            "email": "waiter@waiter.com",
            "name": "Waiter",
            "password": "password"
        }
        serializer = WaiterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        waiter = serializer.save()
        self.assertEqual(waiter.email, data["email"])
        self.assertEqual(waiter.name, data["name"])
        self.assertTrue(waiter.is_staff)
        self.assertTrue(waiter.check_password("password"))

    def test_password_not_returned_in_response(self):
        """ Ensure that password is write-only """
        waiter = Waiter.objects.create_user(
            email="waiter@waiter.com", name="Waiter", password="password"
        )
        serializer = WaiterSerializer(waiter)

        self.assertNotIn("password", serializer.data)

    def test_invalid_email_fails_validation(self):
        """ Invalid email is rejected """
        data = {
            "email": "email@invalid",
            "name": "Waiter",
            "password": "password"
        }
        serializer = WaiterSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_required_fields(self):
        """ Missing required fields result in validation errors """
        data = {}
        serializer = WaiterSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn("email", serializer.errors)
        self.assertIn("password", serializer.errors)

    def test_id_is_read_only(self):
        """ id field is read-only and cannot be set manually."""
        data = {
            "id": 99,
            "email": "waiter@waiter.com",
            "name": "Waiter",
            "password": "password"
        }
        serializer = WaiterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        waiter = serializer.save()
        self.assertNotEqual(waiter.id, 99)
