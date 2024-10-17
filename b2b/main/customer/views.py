from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from main.customer.models import Customer
from .forms import CustomerForm
from main.order.models import Order
from main.address.models import Address

from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def profile(request):
    customer = Customer.objects.get(user=request.user)
    address = Address.objects.filter(customer=customer, default=True).first()

    return render(
        request, "customer/profile.html", {"customer": customer, "address": address}
    )


@login_required
def update_profile(request):
    customer = Customer.objects.get(user=request.user)
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user = User.objects.get(username=request.user.username)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
        messages.success(request, "Your profile was updated.")
        return redirect("customer:profile")

    return render(request, "customer/update_profile.html", {"form": form})


@login_required
def customer_orders(request):
    customer = Customer.objects.get(user=request.user)
    order_list = Order.objects.filter(customer=customer).order_by("-created_date")
    paginator = Paginator(order_list, 12)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    return render(
        request,
        "customer/order_history.html",
        {
            "orders": orders,
        },
    )


@login_required
def get_cart_items(request):
    order_id = request.GET.get("order-id")
    cart = Order.objects.get(order_id=order_id).cart_set.all()

    if request.htmx:
        return render(request, "customer/partials/items.html", {"cart": cart})

    return JsonResponse({"data": list(cart)})
