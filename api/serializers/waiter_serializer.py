from rest_framework import serializers
from api.models.waiter import Waiter


class WaiterSerializer(serializers.ModelSerializer):
    """ Serializer for Waiter model """

    class Meta:
        """ Meta class for Water serialzier """
        model = Waiter
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        """ Call create_user to manage hashing password """
        return Waiter.objects.create_user(**validated_data)
