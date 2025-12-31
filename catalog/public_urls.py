from django.urls import path

from . import public_views


urlpatterns = [
    path("", public_views.product_list, name="product_list"),
    path("products/<slug:slug>/", public_views.product_detail, name="product_detail"),
]
