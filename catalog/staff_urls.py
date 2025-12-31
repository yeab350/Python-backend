from django.urls import path

from . import staff_views


app_name = "catalog_staff"


urlpatterns = [
    path("", staff_views.ProductListView.as_view(), name="product_list"),
    path("new/", staff_views.ProductCreateView.as_view(), name="product_create"),
    path("<slug:slug>/edit/", staff_views.ProductUpdateView.as_view(), name="product_edit"),
    path("<slug:slug>/delete/", staff_views.ProductDeleteView.as_view(), name="product_delete"),
    path("<slug:slug>/toggle-publish/", staff_views.toggle_publish, name="product_toggle"),
]
