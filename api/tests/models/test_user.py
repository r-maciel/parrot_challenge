from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


User = get_user_model()


class TestUser(TestCase):
    """ Tests for User model """

    def test_create_user(self):
        """ Verify correct user creation """
        user = User(
            email="test@email.com", name="Test User"
        )
        user.set_password("password")
        user.full_clean()

        self.assertEqual(user.email, "test@email.com")
        self.assertTrue(user.check_password("password"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_email_is_required(self):
        """ Raise error if not email """
        user = User(
            email=None, name="Test User", password="password"
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_email_is_unique(self):
        """ Email must be unique """
        User.objects.create(
            email="not_unique@email.com",
            name="Test User",
            password="password"
        )

        with self.assertRaises(IntegrityError):
            User.objects.create(
                email="not_unique@email.com",
                name="Test User Two",
                password="password"
            )

    def test_email_is_valid(self):
        """ Email must be in valid format """
        user = User(
            email="test@.com",
            name="Test User",
            password="password"
        )
        with self.assertRaises(ValidationError):
            user.full_clean()
