from django.urls import path
from . import views

app_name = "address"

urlpatterns = [
    # path("", views.address_list, name="address_list"),
    path("", views.address_create, name="address_create"),
    path("address/create/", views.set_default_address, name="address_default"),
]
