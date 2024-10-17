from django import forms
from .models import Shipping



class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ("ship_to",)