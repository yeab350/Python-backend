from django.conf import settings
from django.db import models


class Ticket(models.Model):
	class Status(models.TextChoices):
		OPEN = "open", "Open"
		CLOSED = "closed", "Closed"

	customer_name = models.CharField(max_length=200)
	customer_email = models.EmailField()
	subject = models.CharField(max_length=200)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-updated_at"]

	def __str__(self):
		return f"Ticket #{self.pk}: {self.subject}"


class TicketMessage(models.Model):
	class Sender(models.TextChoices):
		CUSTOMER = "customer", "Customer"
		ADMIN = "admin", "Admin"

	ticket = models.ForeignKey(Ticket, related_name="messages", on_delete=models.CASCADE)
	sender = models.CharField(max_length=20, choices=Sender.choices)
	body = models.TextField()
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="support_messages",
	)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["created_at"]

	def __str__(self):
		return f"{self.get_sender_display()} message ({self.created_at})"
