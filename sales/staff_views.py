from django.contrib import messages
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView

from accounts.mixins import StaffRequiredMixin

from .forms import OrderStatusForm
from .models import Order


class OrderListView(StaffRequiredMixin, ListView):
    model = Order
    template_name = "staff/orders/list.html"
    context_object_name = "orders"

    def get_queryset(self):
        line_total = ExpressionWrapper(
            F("items__unit_price") * F("items__quantity"),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )
        return (
            Order.objects.all()
            .annotate(total=Sum(line_total))
            .prefetch_related("items", "items__product")
        )


def order_detail(request, pk: int):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect("accounts:login")

    order = get_object_or_404(Order.objects.prefetch_related("items", "items__product"), pk=pk)
    form = OrderStatusForm(instance=order)
    return render(request, "staff/orders/detail.html", {"order": order, "form": form})


def update_status(request, pk: int):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect("accounts:login")

    order = get_object_or_404(Order, pk=pk)
    form = OrderStatusForm(request.POST, instance=order)
    if form.is_valid():
        form.save()
        messages.success(request, "Order status updated.")
    else:
        messages.error(request, "Please fix the errors below.")
        return render(request, "staff/orders/detail.html", {"order": order, "form": form})

    return redirect(reverse("sales_staff:order_detail", kwargs={"pk": order.pk}))
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render


def _is_staff(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(_is_staff)
def orders_placeholder(request):
    return render(request, "staff/orders_placeholder.html")
