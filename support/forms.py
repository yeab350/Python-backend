from django import forms

from .models import Ticket


class TicketCreateForm(forms.Form):
    customer_name = forms.CharField(max_length=200)
    customer_email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea, max_length=5000)


class TicketReplyForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, max_length=5000)


class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["status"]
