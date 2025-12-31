from django import forms

from .models import Order


class PublicOrderForm(forms.Form):
    customer_name = forms.CharField(max_length=200)
    customer_email = forms.EmailField()
    quantity = forms.IntegerField(min_value=1, max_value=100, initial=1)


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
