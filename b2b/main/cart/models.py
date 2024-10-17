from django.db import models
from main.order.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(models.Model):
    CANCELLED = "cancel"
    PENDING = "pending"
    APPROVE = "approve"
    DISABLE = "disable"
    OPTIONS = (
        (CANCELLED, "Cancel"),
        (PENDING, "Pending"),
        (APPROVE, "Approve"),
        (DISABLE, "Disable"),
    )
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    size = models.CharField(max_length=10, blank=True)
    image = models.URLField()
    title = models.TextField()
    price = models.CharField(max_length=100)
    original_price = models.CharField(max_length=20, blank=True)
    sales_price = models.CharField(max_length=20, blank=True)
    currency = models.CharField(max_length=20, blank=True)
    shipping_fee = models.IntegerField(null=True, blank=True)
    ordered = models.BooleanField(default=False)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=OPTIONS, default=PENDING)
    shipping = models.BooleanField(default=False)

    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    @property
    def get_price(self):
        return f"{self.currency} {self.price}"

    @property
    def total(self):
        price = self.price.replace(",", "")
        return int(price) * self.quantity

    @property
    def get_total(self):
        price = self.price.replace(",", "")
        return f"{self.currency} {int(price) * self.quantity}"

    @property
    def get_cart_status_display(self):
        if self.status == "cancel":
            return "Cancelled"
        if self.status == "approve":
            return "Approved"
        if self.status == "disable":
            return "Disabled"
        if self.status == "pending":
            return "Pending"

    @property
    def get_css_class(self):
        if self.status == "cancel":
            return "text-danger"
        if self.status == "approve":
            return "text-success"
        if self.status == "pending":
            return "text-primary"
        if self.status == "disable":
            return "text-muted"

    @property
    def is_shipping(self):
        if self.shipping:
            return "item in shipping"
        else:
            return self.get_cart_status_display

    def get_symbol(self):
        word = self.currency
        result = word.find("$")
        return word[result]


def grand_cart_total(user):
    cart = Cart.objects.filter(owner=user, status="approve")
    return sum([x.total for x in cart])
