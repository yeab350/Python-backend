from django.contrib import admin

from .models import Order, Product, Ticket


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "price", "is_published")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("product", "customer_name", "status")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = ("customer_name", "subject", "status")
