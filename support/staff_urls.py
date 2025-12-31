from django.urls import path

from . import staff_views


urlpatterns = [
    path("", staff_views.TicketListView.as_view(), name="ticket_list"),
    path("<int:pk>/", staff_views.ticket_detail, name="ticket_detail"),
    path("<int:pk>/reply/", staff_views.reply, name="ticket_reply"),
    path("<int:pk>/status/", staff_views.update_status, name="ticket_update_status"),
]
