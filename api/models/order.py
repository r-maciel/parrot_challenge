from django.db import models
from api.models.waiter import Waiter
from api.models.customer import Customer
from api.models.product import Product


class Order(models.Model):
    """ Model for Orders """
    waiter = models.ForeignKey(
        Waiter, on_delete=models.PROTECT, related_name="orders"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True
    )
    customer_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through="OrderProduct")

    def __str__(self):
        return f"Order #{self.id}"
