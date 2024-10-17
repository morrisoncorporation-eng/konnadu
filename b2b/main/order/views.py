import json
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from main.customer.models import Customer
from main.cart.models import Cart



@login_required
@csrf_exempt
def order_create(request):
    """
    Create new order populate the customer data
    add cart to order and save to db
    """
    if request.method == "POST":
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.create(customer=customer)
        cart_ids = request.POST.getlist("cartobj")
        approved_items = []
        for item in cart_ids:
            cart = Cart.objects.get(id=item)
            if cart.status == "approve":
                cart.ordered = True
                cart.order = order
                cart.save()                
                approved_items.append(cart.id)
            else:
                cart.status = "cancel"
                cart.save()
            request.session["order_id"] = order.order_id
            request.session["cart_ids"] = approved_items
        return redirect(reverse("order:orders"))
    order = Order.objects.filter(order_id=request.session.get("order_id"))
    return render(request, "order/create.html", {"order": order})

@login_required
def orders(request):
    customer = Customer.objects.get(user=request.user)
    order = (
        Order.objects.filter(customer=customer)
        .exclude(status="C")
        .order_by("-created_date")
    )
    cart_ids = request.session.get("cart_ids")

    
    
    if cart_ids:
        cart_items = Cart.objects.filter(id__in=cart_ids, owner=request.user)

        shipping_total = sum([float(x.shipping_fee) for x in cart_items])
        request.session['shipping_total'] = shipping_total
        print(shipping_total)

        cart = Cart.objects.filter(id__in=cart_ids)
        for item in cart:
            item.shipping=True
            item.save()
    else:
        request.session['shipping_total'] = 0.00
        cart_items = Cart.objects.filter(owner=request.user)
    return render(request, "order/orders.html", {"order": order, "cart_items": cart_items})


@login_required
def order_filter(request):
    if request.htmx:
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.filter(customer=customer)
        status = request.GET.get("order-status")
        if status:
            return render(
                request,
                "order/partials/filter.html",
                {"order": order.filter(status=status)},
            )
        else:
            return render(request, "order/partials/filter.html", {"order": order})
