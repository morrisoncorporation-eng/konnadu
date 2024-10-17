import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from main.cart.models import Cart
from main.order.models import Order
from main.customer.models import Customer
from .forms import ShippingForm
from django.contrib import messages
from main.address.models import Address


@csrf_exempt
@login_required
def shipping_index(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        ids = json.loads(body)
        request.session['cart_ids'] = ids
        return JsonResponse({"response": ids})
    customer = Customer.objects.get(user=request.user)
    address = Address.objects.filter(customer=customer).filter(default=True).first()
    form = ShippingForm()
    items = Cart.objects.filter(id__in=request.session.get("cart_ids"))
    if request.htmx:
        choice = request.GET.get("ship_to")
        if choice == "address":
            address = customer.address_set.first()
            if not address:
                return render(
                    request,
                    "address/partials/message.html",
                )
            else:
                return render(
                    request,
                    "address/partials/default.html",
                )
        elif choice == "global":
            messages.add_message(request, messages.SUCCESS, "Shipping set as global")
            return render(request, "partials/messages.html")
 
    return render(
        request,
        "shipping/index.html",
        {"form": form, "items": items, "address": address},
    )
