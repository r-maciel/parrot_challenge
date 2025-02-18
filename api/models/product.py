from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    """ Model for Products """
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.name
