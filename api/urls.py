from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from api.views.sales_report_views import SalesReportExcelView
from api.views.waiter_view import WaiterView
from api.views.order_view import OrderView


urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("waiters/", WaiterView.as_view(), name="waiters"),
    path("orders/", OrderView.as_view(), name="orders"),
    path("reports/excel/",
         SalesReportExcelView.as_view({'get': 'list'}),
         name="sales_report_excel"),
]
