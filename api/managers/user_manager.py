from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    """

    def create_user(self, email, name, password=None, **extra_fields):
        """ Create user verifying email """
        if not email:
            raise ValueError("Email is missing")
        if not name:
            raise ValueError("Name is missing")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """ Create and save a superuser """
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True

        return self.create_user(email, name, password, **extra_fields)
