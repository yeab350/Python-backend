from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "is_published"]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None:
            return price
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price
