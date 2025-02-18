from django.db import models


class Customer(models.Model):
    """ Customer model (not authenticated users, for future iterations) """
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.email
