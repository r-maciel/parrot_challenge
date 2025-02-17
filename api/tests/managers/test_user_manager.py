from django.test import TestCase
from django.db.utils import IntegrityError
from api.managers.user_manager import UserManager
from api.models.user import User


class TestUserManager(TestCase):
    """ Tests for UserManager """

    @classmethod
    def setUpTestData(cls):
        """ Initializing just once """
        cls.manager = UserManager()
        cls.manager.model = User

    def test_create_user(self):
        """ Create user correctly """
        user = self.manager.create_user(
            email="test@email.com",
            name="Test User",
            password="password"
        )

        self.assertEqual(user.email, "test@email.com")
        self.assertTrue(user.check_password("password"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_email_is_required(self):
        """ Raise error if not email """
        with self.assertRaises(ValueError):
            self.manager.create_user(
                email=None,
                name="Test User",
                password="password"
            )

    def test_email_is_unique(self):
        """ Email must be unique """
        self.manager.create_user(
            email="not_unique@email.com",
            name="Test User",
            password="password"
        )

        with self.assertRaises(IntegrityError):
            self.manager.create_user(
                email="not_unique@email.com",
                name="Test User Two",
                password="password"
            )

    def test_create_user_with_normalized_email(self):
        """ Email is normalized before saving """
        user = self.manager.create_user(
            email="test@EMAIL.COM", name="Test User", password="password"
        )

        self.assertEqual(user.email, "test@email.com")

    def test_name_is_required(self):
        """ Name is required """
        with self.assertRaises(ValueError):
            self.manager.create_user(
                email="test@email.com",
                name="",
                password="password"
            )

    def test_create_superuser(self):
        """ Create superuser correctly """
        superuser = self.manager.create_superuser(
            email="admin@example.com",
            name="Admin User",
            password="adminpassword"
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertEqual(superuser.name, "Admin User")
        self.assertTrue(superuser.check_password("adminpassword"))
