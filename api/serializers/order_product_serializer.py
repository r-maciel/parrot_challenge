from rest_framework import serializers
from api.models.order_product import OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    """ Serializer for OrderProduct model """
    name = serializers.CharField(source="product.name")
    price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        write_only=True,
    )
    quantity = serializers.IntegerField(min_value=0, default=1)

    class Meta:
        """Meta class for Product serializer."""
        model = OrderProduct
        fields = ["name", "quantity", "price_at_order", "price"]
        read_only_fields = ["price_at_order"]
