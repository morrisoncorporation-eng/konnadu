import uuid
from django.db import models
from django.urls import reverse
from main.customer.models import Customer


def order_id_generator():
    return uuid.uuid4().hex[:11].upper()


class Order(models.Model):
    CANCELLED = "C"
    FULFILLED = "F"
    PROCESSING = "P"
    NEW = "N"
    OPTIONS = [
        (CANCELLED, "Cancelled"),
        (FULFILLED, "Fulfilled"),
        (PROCESSING, "Processing"),
        (NEW, "New"),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=11, unique=True, default=order_id_generator)
    status = models.CharField(default=OPTIONS[3][0], choices=OPTIONS, max_length=12)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

    @property
    def get_fulfilled(self):
        if not self.fulfilled:
            return "No"
        return "Yes"

    @property
    def get_cancelled(self):
        if not self.cancelled:
            return "No"
        return "Yes"

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})

    def get_total(self):
        return "total"
