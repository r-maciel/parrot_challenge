from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.serializers.order_serializer import OrderSerializer


class OrderView(APIView):
    """ View to create orders """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        """Handles order creation."""
        serializer = OrderSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
