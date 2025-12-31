from django.urls import include, path

from . import staff_views


app_name = "staff"


urlpatterns = [
    path("", staff_views.dashboard, name="dashboard"),
    path("products/", include(("catalog.staff_urls", "catalog_staff"))),
    path("orders/", include(("sales.staff_urls", "sales_staff"))),
    path("tickets/", include(("support.staff_urls", "support_staff"))),
]
