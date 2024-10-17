from django import forms
from .models import Customer


class DateInput(forms.DateInput):
    input_type = "date"


class CustomerForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=DateInput)

    class Meta:
        model = Customer
        exclude = ("user",)
