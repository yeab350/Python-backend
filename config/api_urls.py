from __future__ import annotations

from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from accounts.api_views import logout, me
from config.api_views import health
from catalog.api import ProductViewSet
from sales.api import OrderViewSet
from support.api import TicketViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("health/", health, name="api_health"),
    path("auth/token/", obtain_auth_token, name="api_token"),
    path("auth/me/", me, name="api_me"),
    path("auth/logout/", logout, name="api_logout"),
    path("", include(router.urls)),
]
