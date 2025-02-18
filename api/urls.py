from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from api.views.waiter_view import WaiterView
from api.views.order_view import OrderView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("waiters/", WaiterView.as_view()),
    path("orders/", OrderView.as_view()),
]
