from datetime import datetime
from django.db.models.aggregates import Sum
from django.core.exceptions import BadRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer
from api.permissions import IsSuperUser
from api.serializers.sales_report_serializer import SalesReportSerializer
from api.models.order_product import OrderProduct


class SalesReportExcelView(XLSXFileMixin, ReadOnlyModelViewSet):
    """ View for excel report """
    permission_classes = [IsAuthenticated, IsSuperUser]
    renderer_classes = (XLSXRenderer,)
    serializer_class = SalesReportSerializer
    filename = 'sales_report.xlsx'

    def get_queryset(self):
        """ Get queryset for the sales report """

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if not start_date or not end_date:
            raise BadRequest(
                "Both start_date and end_date query parameters are required."
            )
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            raise BadRequest("Invalid date format. Use YYYY-MM-DD.")

        if start_date > end_date:
            raise BadRequest("start_date must be before or equal to end_date.")

        return OrderProduct.objects.filter(
            order__created_at__range=[start_date, end_date]
        ).values("product__name").annotate(
            quantity_sold=Sum("quantity"),
            total=Sum("subtotal")
        ).order_by("-quantity_sold")
