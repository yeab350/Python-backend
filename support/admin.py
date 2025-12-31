from django.contrib import admin

from .models import Ticket, TicketMessage


class TicketMessageInline(admin.TabularInline):
	model = TicketMessage
	extra = 0
	readonly_fields = ("sender", "created_by", "created_at")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = ("id", "subject", "customer_email", "status", "updated_at")
	list_filter = ("status",)
	search_fields = ("subject", "customer_email", "customer_name")
	inlines = [TicketMessageInline]
