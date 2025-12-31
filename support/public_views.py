from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import TicketCreateForm
from .models import Ticket, TicketMessage


def ticket_create(request):
    if request.method == "POST":
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            ticket = Ticket.objects.create(
                customer_name=form.cleaned_data["customer_name"],
                customer_email=form.cleaned_data["customer_email"],
                subject=form.cleaned_data["subject"],
            )
            TicketMessage.objects.create(
                ticket=ticket,
                sender=TicketMessage.Sender.CUSTOMER,
                body=form.cleaned_data["message"],
            )
            return redirect(reverse("support_public:ticket_success", kwargs={"pk": ticket.pk}))
    else:
        form = TicketCreateForm()

    return render(request, "public/ticket_create.html", {"form": form})


def ticket_success(request, pk: int):
    return render(request, "public/ticket_success.html", {"ticket_id": pk})
