from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from main.customer.models import Customer

User = get_user_model()


class Address(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)
    phone_number = PhoneNumberField(blank=True)
    country = CountryField(blank=True)
    address = models.CharField(max_length=350, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    zip_code_or_postal_code = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name_plural = "Address"

    def __str__(self):
        return self.address