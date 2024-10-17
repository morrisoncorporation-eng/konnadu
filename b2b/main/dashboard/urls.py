from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('',  views.index, name="index"),
    path('order/<str:order_id>', views.dashboard_order, name="dashboard-order"),
    path('dashboard-carts/', views.dashboard_carts, name="dashboard-carts"),
    path('customers/', views.dashboard_customers, name="dasboard-customers"),
    path('order/summary/', views.order_summary, name="order_summary"),
]