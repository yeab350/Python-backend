from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from catalog.models import Product

from .forms import PublicOrderForm
from .models import Order, OrderItem


def create_order(request, product_slug: str):
    product = get_object_or_404(Product, slug=product_slug, is_published=True)

    if request.method == "POST":
        form = PublicOrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                customer_name=form.cleaned_data["customer_name"],
                customer_email=form.cleaned_data["customer_email"],
            )
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=form.cleaned_data["quantity"],
                unit_price=product.price,
            )
            return redirect(reverse("sales_public:order_success", kwargs={"pk": order.pk}))
    else:
        form = PublicOrderForm()

    return render(
        request,
        "public/order_create.html",
        {
            "product": product,
            "form": form,
        },
    )


def order_success(request, pk: int):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "public/order_success.html", {"order": order})
