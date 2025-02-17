from django.test import TestCase
from api.models.user import User
from api.models.waiter import Waiter


class TestWaiter(TestCase):
    """Tests para el Proxy Model `Waiter`"""

    def test_create_waiter(self):
        """ Verify correct waiter creation """
        waiter = Waiter.objects.create_user(
            email="waiter@waiter.com", name="Waiter", password="password"
        )

        self.assertTrue(waiter.is_staff)
        self.assertIsInstance(waiter, Waiter)
        self.assertIsInstance(waiter, User)
        self.assertEqual(Waiter.objects.count(), 1)

    def test_waiter_is_saved_with_is_staff_true(self):
        """ Verify `save()` sets `is_staff=True`"""
        waiter = Waiter(
            email="waiter@waiter.com", name="Waiter", password="password"
        )
        waiter.is_staff = False
        waiter.save()

        self.assertTrue(waiter.is_staff)
        self.assertEqual(Waiter.objects.count(), 1)
