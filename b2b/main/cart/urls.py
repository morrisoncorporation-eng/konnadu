from django.urls import path
from  . import views

app_name = "cart"

urlpatterns = [
    path('', views.cart, name="cart"),
    path('create/', views.cart_create, name="cart-create"),
    path('delete/', views.cart_delete, name="cart-delete"),
    path('cart-detail/<int:cart_id>/', views.cart_detail, name="cart-detail"),
    path('user-auth-check/', views.user_auth_check, name="user_auth_check"),
    path('update/quantity', views.cart_update_quantity, name="update-qty"),
    path("cart/action/", views.cart_action, name="action"),
]