from django import forms
from main.cart.models import Cart
from main.order.models import Order

class DateInput(forms.DateInput):
    input_type = "date"

class CartStatusForm(forms.Form):
    cart_status = forms.ChoiceField(choices=Cart.OPTIONS, required=False)
    created = forms.DateTimeField(
        help_text="Cart created date",
        required=False,
        widget = DateInput,
    )
    customer = forms.CharField(required=False, help_text="Customer username")

class OrderStatusForm(forms.Form):
    status = forms.ChoiceField(choices=Order.OPTIONS, required=False)
    created_date = forms.DateTimeField(
        help_text="Cart created date",
        required=False,
        widget = DateInput,
    )
    order_number = forms.CharField(required=False, help_text="Order # eg: 59FAB63AAE0")
    customer = forms.CharField(required=False, help_text="Customer username")

class CartActionForm(forms.Form):
    cart_status = forms.ChoiceField(choices=Cart.OPTIONS, required=False)