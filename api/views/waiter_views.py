from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from api.serializers.waiter_serializer import WaiterSerializer
from api.permissions import IsSuperUser


class WaiterCreateView(CreateAPIView):
    """ Manage waiter instances """
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = WaiterSerializer
