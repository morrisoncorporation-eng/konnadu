from django.urls import path
from . import views
app_name = "shipping"

urlpatterns = [
    path('', views.shipping_index, name="shipping-index"),
]