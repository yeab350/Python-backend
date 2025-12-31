from decimal import Decimal

from django.db import models
from django.db.models import Sum

from catalog.models import Product


class Order(models.Model):
	class Status(models.TextChoices):
		PENDING = "pending", "Pending"
		COMPLETED = "completed", "Completed"

	customer_name = models.CharField(max_length=200)
	customer_email = models.EmailField()
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"Order #{self.pk}"

	def total_amount(self) -> Decimal:
		total = (
			self.items.aggregate(
				total=Sum(models.F("unit_price") * models.F("quantity"))
			).get("total")
			or Decimal("0.00")
		)
		return total


class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	quantity = models.PositiveIntegerField()
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"{self.product.name} x {self.quantity}"

	def line_total(self) -> Decimal:
		return self.unit_price * self.quantity
