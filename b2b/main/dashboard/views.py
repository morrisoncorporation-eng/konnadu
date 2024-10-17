from datetime import datetime
from django.http.response import JsonResponse
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from main.customer.models import Customer
from django.views.decorators.csrf import csrf_exempt
from main.order.models import Order
from main.cart.models import Cart
from main.emails.views import cart_update_user
from .forms import CartStatusForm, OrderStatusForm, CartActionForm

from_email = settings.EMAIL_HOST_USER


@login_required
def index(request):
    status = Cart()
    cart = Cart.objects.all()
    pending = cart.filter(status=status.PENDING).count()
    approved = cart.filter(status=status.APPROVE).count()
    disabled = cart.filter(status=status.DISABLE).count()
    cancelled = cart.filter(status=status.CANCELLED).count()
    ctx = {
        "pending": pending,
        "approved": approved,
        "disabled": disabled,
        "cancelled": cancelled,
    }
    return render(request, "dashboard/index.html", ctx)


@csrf_exempt
@login_required
def dashboard_carts(request):
    cart_action = CartActionForm(request.GET)
    cart_status_filter = CartStatusForm(request.GET)
    cart_qs = Cart.objects.all().order_by("-created")
    paginator = Paginator(cart_qs, 20)
    page_number = request.GET.get("page")
    carts = paginator.get_page(page_number)
    if request.htmx:
        if request.GET.get("customer"):
            customer = request.GET.get("customer")
            carts = Cart.objects.filter(owner__username__icontains=customer)

        if request.GET.get("cart_status"):
            status = request.GET.get("cart_status")
            carts = Cart.objects.filter(status=status)

        if request.GET.get("created"):
            created = request.GET.get("created")
            carts = Cart.objects.filter(created__date=created)
        return render(
            request,
            "dashboard/partials/carts-partial.html",
            {"carts": carts, "cart_action": cart_action},
        )
    if request.method == "POST":
        cart_id = request.POST.get("cart_id")
        reason = request.POST.get("reason")
        shipping = request.POST.get("shipping")
        cart_status = request.POST.get("cart_status")
        cart = Cart.objects.get(id=cart_id)
        if reason:
            cart.reason = reason
        else:
            cart.reason = ""
        if shipping:
            cart.shipping_fee = shipping
        else:
            cart.shipping = 0
        cart.status = cart_status
        cart.save()
        to_email = cart.owner.email
        cart_update_user(from_email, to_email, cart, cart_status)

        return JsonResponse(
            {
                "cart": cart.id,
                "success": "updated succesfully",
                "email": f"email sent to {cart.owner}",
            },
            status=201,
        )

    # else:
    #     return redirect(reverse("dashboard:dashboard-orders"))

    ctx = {"form": cart_status_filter, "carts": carts, "cart_action": cart_action}
    return render(request, "dashboard/orders.html", ctx)


@login_required
def dashboard_order(request, order_id):
    order = Order.objects.get(order_id=order_id)
    return render(request, "dashboard/order.html", {"order": order})


@login_required
def dashboard_customers(request):
    return render(request, "dashboard/customers.html")


def order_summary(request):
    form = OrderStatusForm()
    orders = Order.objects.all().order_by("-created_date")
    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    order_summary = paginator.get_page(page_number)
    if request.htmx:
        if request.GET.get("status"):
            order_summary = Order.objects.filter(status=request.GET.get("status"))
        elif request.GET.get("created_date"):
            order_summary = Order.objects.filter(
                created_date__date=request.GET.get("created_date")
            )
        elif request.GET.get("order_number"):
            order_summary = Order.objects.filter(order_id=request.GET.get("order_number"))
        elif request.GET.get("customer"):
            order_summary = Order.objects.filter(
                customer__user__username=request.GET.get("customer")
            )
        return render(
            request,
            "dashboard/partials/order-summary-partial.html",
            {"order_summary": order_summary},
        )
    ctx = {"form": form, "order_summary": order_summary}
    return render(request, "dashboard/order_summary.html", ctx)
