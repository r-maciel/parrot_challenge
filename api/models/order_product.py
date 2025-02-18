from django.db import models
from django.core.validators import MinValueValidator
from api.models.order import Order
from api.models.product import Product


class OrderProduct(models.Model):
    """ Intermediate table for Order and Product ManyToMany relationship """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_products"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    class Meta:
        unique_together = ("order", "product")
