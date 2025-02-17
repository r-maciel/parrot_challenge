from django.contrib.auth.models import AbstractUser
from django.db import models
from api.managers.user_manager import UserManager


class User(AbstractUser):
    """ Custom User model """
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return self.email
