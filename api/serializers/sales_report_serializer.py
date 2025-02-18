from rest_framework import serializers


class SalesReportSerializer(serializers.Serializer):
    """ Serializer for sales report """

    product_name = serializers.CharField(source="product__name")
    quantity_sold = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
