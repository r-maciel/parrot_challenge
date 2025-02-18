from functools import cached_property
from api.models.order import Order
from api.models.customer import Customer
from api.models.product import Product
from api.models.order_product import OrderProduct


class OrderCreator:
    @classmethod
    def create(cls, context, validated_data):
        """ Class method for quick access """
        return OrderCreator(context, validated_data).create_order()

    def __init__(self, context, validated_data):
        self.context = context
        self.validated_data = validated_data

    def create_order(self):
        """ Creates the order and all its related objects """
        order_data = self.get_order_data()
        order = Order.objects.create(**order_data)

        self.create_products_in_bulk()
        products = self.recover_all_order_products()
        self.create_order_products_in_bulk(order, products)

        return Order.objects.prefetch_related(
            "order_products__product"
        ).get(id=order.id)


    def recover_all_order_products(self):
        """
        Recover all the products for the order, those who were created,
        and those who were already in the DB
        """
        product_names = self.products_data.keys()
        return Product.objects.filter(name__in=product_names)

    def create_order_products_in_bulk(self, order, products):
        """ Create order-products in bulk """
        order_products = [
            OrderProduct(
                product=product,
                order=order,
                price_at_order=product.price,
                quantity=self.products_data[product.name]["quantity"],
                subtotal=product.price*self.products_data[product.name]["quantity"]
            ) for product in products
        ]
        OrderProduct.objects.bulk_create(order_products)

    def create_products_in_bulk(self):
        """ Create products in bulk """
        products_to_create = [Product(name=name, price=data["price"])
                              for name, data in self.products_data.items()]
        Product.objects.bulk_create(products_to_create, ignore_conflicts=True)

    def get_waiter_from_request(self):
        """ Get waiter from request context """
        request = self.context.get("request")

        return request.user

    def get_order_data(self):
        """ Data for create Order object """
        customer_email = self.validated_data.get("customer_email", None)
        customer_name = self.validated_data.get("customer_name")
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

    @cached_property
    def products_data(self):
        """
        Get a dict with unique products, with price and quantity per product
        """
        product_map = {}
        for product in self.validated_data["order_products"]:
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

