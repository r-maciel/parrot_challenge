from rest_framework import serializers
from api.models.order import Order
from api.models.customer import Customer
from api.models.product import Product
from api.models.order_product import OrderProduct
from api.serializers.order_product_serializer import OrderProductSerializer


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
        order_data = self.get_order_data(validated_data)
        order = Order.objects.create(**order_data)

        products_data = self.clean_products_data(validated_data["order_products"])
        products_to_create = [Product(name=name, price=data["price"])
                              for name, data in products_data.items()]
        Product.objects.bulk_create(products_to_create, ignore_conflicts=True)

        product_names = products_data.keys()
        products = Product.objects.filter(name__in=product_names)

        order_products = [
            OrderProduct(
                product=product,
                order=order,
                price_at_order=product.price,
                quantity=products_data[product.name]["quantity"],
                subtotal=product.price*products_data[product.name]["quantity"]
            ) for product in products
        ]
        OrderProduct.objects.bulk_create(order_products)

        return Order.objects.prefetch_related(
            "order_products__product"
        ).get(id=order.id)

    def get_waiter_from_request(self):
        """ Get waiter from request context """
        request = self.context.get("request")

        return request.user

    def get_order_data(self, validated_data):
        """ Data for create Order object """
        customer_email = validated_data.get("customer_email", None)
        customer_name = validated_data.get("customer_name")
        data = {
            'waiter': self.get_waiter_from_request(),
            'customer_name': customer_name
        }

        if customer_email:
            data['customer'], _ = Customer.objects.get_or_create(
                email=customer_email,
                defaults={"name": customer_name}
            )

        return data

    def clean_products_data(self, products):
        """
        Get a dict with unique products, with price and quantity per product
        """
        product_map = {}
        for product in products:
            name = product['product']['name']
            price = product['product']['price']
            quantity = product['quantity']

            if name in product_map:
                product_map[name]['quantity'] += quantity
                continue

            product_map[name] = {
                'price': price,
                'quantity': quantity
            }

        return product_map
