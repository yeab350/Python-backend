from django.db import models


class Product(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	is_published = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return self.name


class Order(models.Model):
	class Status(models.TextChoices):
		PENDING = "pending", "Pending"
		COMPLETED = "completed", "Completed"

	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	quantity = models.IntegerField()
	customer_name = models.CharField(max_length=200)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Order #{self.pk} - {self.customer_name}"


class Ticket(models.Model):
	class Status(models.TextChoices):
		OPEN = "open", "Open"
		CLOSED = "closed", "Closed"

	customer_name = models.CharField(max_length=200)
	subject = models.CharField(max_length=200)
	message = models.TextField()
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Ticket #{self.pk} - {self.subject}"

# Create your models here.
