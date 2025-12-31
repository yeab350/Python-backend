from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView

from accounts.mixins import StaffRequiredMixin

from .forms import TicketReplyForm, TicketStatusForm
from .models import Ticket, TicketMessage


class TicketListView(StaffRequiredMixin, ListView):
    model = Ticket
    template_name = "staff/tickets/list.html"
    context_object_name = "tickets"

    def get_queryset(self):
        return Ticket.objects.all()


def ticket_detail(request, pk: int):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect("accounts:login")

    ticket = get_object_or_404(Ticket.objects.prefetch_related("messages"), pk=pk)
    reply_form = TicketReplyForm()
    status_form = TicketStatusForm(instance=ticket)
    return render(
        request,
        "staff/tickets/detail.html",
        {"ticket": ticket, "reply_form": reply_form, "status_form": status_form},
    )


def reply(request, pk: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect("accounts:login")

    ticket = get_object_or_404(Ticket, pk=pk)
    form = TicketReplyForm(request.POST)
    if form.is_valid():
        TicketMessage.objects.create(
            ticket=ticket,
            sender=TicketMessage.Sender.ADMIN,
            body=form.cleaned_data["message"],
            created_by=request.user,
        )
        messages.success(request, "Reply sent.")
    else:
        messages.error(request, "Please fix the errors below.")
        ticket = Ticket.objects.prefetch_related("messages").get(pk=pk)
        status_form = TicketStatusForm(instance=ticket)
        return render(
            request,
            "staff/tickets/detail.html",
            {"ticket": ticket, "reply_form": form, "status_form": status_form},
        )

    return redirect(reverse("support_staff:ticket_detail", kwargs={"pk": pk}))


def update_status(request, pk: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect("accounts:login")

    ticket = get_object_or_404(Ticket, pk=pk)
    form = TicketStatusForm(request.POST, instance=ticket)
    if form.is_valid():
        form.save()
        messages.success(request, "Ticket status updated.")
    else:
        messages.error(request, "Please fix the errors below.")
        ticket = Ticket.objects.prefetch_related("messages").get(pk=pk)
        reply_form = TicketReplyForm()
        return render(
            request,
            "staff/tickets/detail.html",
            {"ticket": ticket, "reply_form": reply_form, "status_form": form},
        )

    return redirect(reverse("support_staff:ticket_detail", kwargs={"pk": pk}))
