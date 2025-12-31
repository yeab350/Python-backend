from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.mixins import StaffRequiredMixin

from .forms import ProductForm
from .models import Product


class ProductListView(StaffRequiredMixin, ListView):
    model = Product
    template_name = "staff/products/list.html"
    context_object_name = "products"


class ProductCreateView(StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "staff/products/form.html"

    def get_success_url(self):
        messages.success(self.request, "Product created.")
        return reverse("catalog_staff:product_list")


class ProductUpdateView(StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "staff/products/form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        messages.success(self.request, "Product updated.")
        return reverse("catalog_staff:product_list")


class ProductDeleteView(StaffRequiredMixin, DeleteView):
    model = Product
    template_name = "staff/products/confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        messages.success(self.request, "Product deleted.")
        return reverse("catalog_staff:product_list")


def toggle_publish(request, slug: str):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect("accounts:login")

    product = get_object_or_404(Product, slug=slug)
    product.is_published = not product.is_published
    product.save(update_fields=["is_published", "updated_at"])
    state = "published" if product.is_published else "unpublished"
    messages.success(request, f"Product {state}.")
    return redirect("catalog_staff:product_list")
