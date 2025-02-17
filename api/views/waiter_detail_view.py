from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.serializers.waiter_serializer import WaiterSerializer
from api.permissions import IsSuperUser


class WaiterDetailView(APIView):
    """ Manage waiter instances """
    permission_classes = [IsAuthenticated, IsSuperUser]

    def post(self, request):
        """ Create waiter """
        serializer = WaiterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
