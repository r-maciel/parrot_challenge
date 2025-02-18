from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.serializers.order_serializer import OrderSerializer
from api.models.order import Order


class OrderView(ListCreateAPIView):
    """ View to create orders """
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Order.objects.prefetch_related("order_products__product")
    serializer_class = OrderSerializer

    def get_serializer_context(self):
        """ Pass context to serializer """
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
