from django.urls import path
from . import views

app_name = "customer"

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("profile/update", views.update_profile, name="update-profile"),
    path("order-history", views.customer_orders, name="my-orders"),
    path("api/order-cart-items", views.get_cart_items, name="get-cart-items"),
]
