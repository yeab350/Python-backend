from django.db import models
from django.utils.text import slugify


class Product(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=220, unique=True, db_index=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	is_published = models.BooleanField(default=False, db_index=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-updated_at"]

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			base_slug = slugify(self.name)[:200] or "product"
			slug = base_slug
			suffix = 2
			while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
				slug = f"{base_slug}-{suffix}"
				suffix += 1
			self.slug = slug
		super().save(*args, **kwargs)

# Create your models here.
