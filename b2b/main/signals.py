import re
from django.dispatch import receiver
from django.db import models
from .utils import unique_slug_generator
from .market import Store
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from main.customer.models import Customer
from main.order.models import Order
from main.cart.models import Cart


User = get_user_model()


@receiver(post_save, sender=User)
def create_new_customer_signals(sender, created, instance, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(models.signals.pre_save, sender=Store)
def auto_slug_generator_good(sender, instance, **kwargs):
    """
    Creates a slug if there is no slug.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(models.signals.pre_save, sender=Store)
def auto_slug_generator_page(sender, instance, **kwargs):
    """
    Creates a slug if there is no slug.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(models.signals.post_save, sender=Order)
def order_created_signal(sender, instance, **kwargs):

    """
    Notify admins that a new order has been created.
    """
    pass


@receiver(models.signals.pre_save, sender=Cart)
def cart_created_signal(sender, instance, **kwargs):
    price = re.sub('[$£,USD]', '', instance.price)
    instance.currency = instance.price
    instance.price = price
