from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "price", "is_published", "updated_at")
	list_filter = ("is_published",)
	search_fields = ("name", "slug")
	prepopulated_fields = {"slug": ("name",)}
