from rest_framework import serializers
from api.serializers.order_product_serializer import OrderProductSerializer
from api.services.order_creator import OrderCreator
from api.models.order import Order


class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for Order model, handling Customer and Products creation """

    customer_email = serializers.EmailField(write_only=True, required=False)
    customer_name = serializers.CharField()
    waiter = serializers.StringRelatedField()
    products = OrderProductSerializer(many=True, source="order_products")
    total = serializers.SerializerMethodField()

    class Meta:
        """ Meta class for order serializer """
        model = Order

        fields = [
            "id",
            "waiter",
            "customer_email",
            "customer_name",
            "products",
            "total",
            "created_at"
        ]
        read_only_fields = ["id", "waiter", "created_at", "total"]

    def get_total(self, obj):
        """ Calculate total based on order products """
        return sum(item.subtotal for item in obj.order_products.all())

    def validate_products(self, value):
        """ Validate products is not empty """
        if not value:
            raise serializers.ValidationError("The order must contain at least one product")
        return value

    def create(self, validated_data):
        """ Override create method for custom creation """
        return OrderCreator.create(
            context=self.context, validated_data=validated_data
        )
