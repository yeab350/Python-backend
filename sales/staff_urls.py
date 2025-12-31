from django.urls import path

from . import staff_views


app_name = "sales_staff"


urlpatterns = [
    path("", staff_views.OrderListView.as_view(), name="order_list"),
    path("<int:pk>/", staff_views.order_detail, name="order_detail"),
    path("<int:pk>/status/", staff_views.update_status, name="order_update_status"),
]
