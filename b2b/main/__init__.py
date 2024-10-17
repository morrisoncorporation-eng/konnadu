from django.core.exceptions import AppRegistryNotReady

try:
    from .customer.models import Customer
    from .pages.models import Page #SiteConfiguration
    from .order.models import Order
    from .cart.models import Cart
    from .shipping.models import Shipping
    from .address.models import Address
except AppRegistryNotReady:
    pass

default_app_config = "main.apps.MainConfig"