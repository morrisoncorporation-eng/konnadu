from django.db import models
from main.order.models import Order
from main.address.models import Address


class Shipping(models.Model):
    ADDRESS = "address"
    GLOBAL = "global"
    OPTIONS = [
        (ADDRESS, "My address"), 
        (GLOBAL, "Global")
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ship_to = models.CharField(choices=OPTIONS, max_length=7)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Shipping"

    def __str__(self):
        return f'#{self.order} to {self.address}'
