from django.shortcuts import get_object_or_404, render

from .models import Product


def product_list(request):
    products = Product.objects.filter(is_published=True).order_by("name")
    return render(request, "public/product_list.html", {"products": products})


def product_detail(request, slug: str):
    product = get_object_or_404(Product, slug=slug, is_published=True)
    return render(request, "public/product_detail.html", {"product": product})
