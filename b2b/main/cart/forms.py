from django import forms
from .models import Cart

class CartEditForm(forms.ModelForm):
    class Meta:
        model = Cart
        exclude = ("status", ) 