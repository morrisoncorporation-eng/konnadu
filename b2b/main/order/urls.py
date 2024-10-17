from django.urls import path
from . import views
app_name = "order"

urlpatterns = [
    path('create/', views.order_create, name="create"),
    path('orders/', views.orders, name="orders"),
    path('filter', views.order_filter, name="order-filter"),
]