import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils import timezone
from main.emails.views import new_cart_item_email
from .models import Cart
from .forms import CartEditForm

User = get_user_model()
today = timezone.now().date()

from_email = settings.EMAIL_HOST_USER
to_emails = User.objects.filter(is_staff=True).values_list("email", flat=True)


@login_required
def cart(request):
    approved = ""
    approved_total = float()
    # get all carts and group by date created...
    # check if items with similar name is already in the cart to increase their value
    cart_items = Cart.objects.filter(owner=request.user).order_by("status")
    if cart_items.filter(status="approve", shipping=False):
        approved = True
        approved_total = sum(
            [
                int(x.quantity) * float(x.price)
                for x in Cart.objects.filter(
                    owner=request.user, status="approve"
                ).order_by("status")
            ]
        )
        
        request.session["approved_total"] = "{:.2f}".format(approved_total)
        request.session.modified = True

    cart_sum = sum(
        [
            int(x.quantity) * float(x.price)
            for x in Cart.objects.filter(owner=request.user).order_by("status")
        ]
    )

    return render(
        request,
        "cart/index.html",
        {
            "cart_items": cart_items,
            "approved": approved,
            "approved_total": approved_total,
            "cart_sum": cart_sum,
        },
    )


@csrf_exempt
def user_auth_check(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        content = json.loads(body)
        data = content["user"]
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

        data = {
            "username": username,
            "password": password,
        }

    return JsonResponse(data, status=200)


@csrf_exempt
def cart_create(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        content = json.loads(body)
        try:
            user_client = content["user"]
            username = user_client.get("username")
            password = user_client.get("password")
            user = authenticate(request, username=username, password=password)
            remote_cart = content["cart"]
            item_ids = []
            if user:
                for item in remote_cart:
                    try:
                        cart_obj = Cart.objects.get(
                            owner__username=user.username,
                            title=item.get("title"),
                            shop_name=item.get("name"),
                        )
                        # cart_obj.quantity += int(item.get("quantity"))
                        # cart_obj.save()
                        # item_ids.append(cart_obj.id)
                        print(cart_obj)
                        new_cart_item_email(from_email, to_emails, item_ids)
                    except ObjectDoesNotExist:
                        cart = Cart(
                            owner=user,
                            status="pending",
                            title=item.get("title"),
                            image=item.get("image"),
                            shop_name=item.get("name"),
                            quantity=item.get("quantity"),
                            price=item.get("price"),
                        )
                        print(f"{cart} No obj")
                        cart.save()
                        item_ids.append(cart.id)
                        new_cart_item_email(from_email, to_emails, item_ids)
                return JsonResponse({"success": "created"}, status=200)
            else:
                return JsonResponse({"error": "forbidden"}, status=403)
        except ObjectDoesNotExist:
            return JsonResponse({"user": "Not found"}, status=404)
    return JsonResponse({"success": "Created"}, status=200)


# @login_required
# def cart_delete(request):
#     return JsonResponse({"success": "Cleared"}, status=200)


@csrf_exempt
@login_required
def cart_delete(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        ids = json.loads(body)
        items = Cart.objects.filter(id__in=ids)
        for item in items:
            item.delete()
    return JsonResponse({"message": "items deleted", "items": ids}, status=201)


@login_required
def cart_detail(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    form = CartEditForm(instance=cart)
    if request.method == "POST":
        form.save()
        return redirect(reverse("cart:cart-detail", cart_id=cart.id))
    return render(request, "cart/cart-detail.html", {"cart": cart, "form": form})


@login_required
@csrf_exempt
def cart_update_quantity(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        content = json.loads(body)
        item_id = content["id"]
        try:
            item = Cart.objects.get(id=item_id)
            item.quantity = content["quantity"]
            item.save()

            print(item.total)
            data = {
                "total": item.get_total,
            }
            return JsonResponse({"data": data}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"err": "Something went wrong"}, status=404)


@csrf_exempt
@login_required
def cart_action(request):
    if request.method == "POST":
        body = request.body.decode("utf-8")
        content = json.loads(body)
        deleted = []
        action = content.get("action")
        if action == "delete":
            items = content.get("items")
            for item in items:
                cart = Cart.objects.get(id=item)
                deleted.append(cart.id)
                cart.delete()
        elif action == "update":
            items = content.get("items")
            for item in items:
                cart = Cart.objects.get(id=item.get("id"))
                cart.quantity = int(item.get("qty"))
                cart.save()
        else:
            error = "error"
        response = {"action": action, "message": "Completed!", "deleted": deleted}
        return JsonResponse(response, status=200, safe=False)
