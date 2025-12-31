from django.urls import path

from . import public_views


urlpatterns = [
    path("new/<slug:product_slug>/", public_views.create_order, name="order_create"),
    path("success/<int:pk>/", public_views.order_success, name="order_success"),
]
