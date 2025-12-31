from django.urls import path

from . import public_views


urlpatterns = [
    path("", public_views.ticket_create, name="ticket_create"),
    path("success/<int:pk>/", public_views.ticket_success, name="ticket_success"),
]
