from django.db import models
from django.contrib.auth import get_user_model
# from solo.models import SingletonModel
from main.market.models import Store

User = get_user_model()


class Page(models.Model):
    """
    Use for managing and grouping pages.
    Example page `featured` will be grouped Stores listed in featured.
    """
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    store = models.ManyToManyField(Store, blank=True)
    max_items = models.PositiveSmallIntegerField(default=10)
    popularity = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Store Category"
        verbose_name_plural = "Store Categories"
        ordering = ("-id", "created_date")
        db_table = "page"



class Jumbotron(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3    
    ORDER_CHOICES = (
        (ONE, "One"),
        (TWO, "Two"),
        (THREE, "Three"),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="jumbotron/")
    order = models.IntegerField(unique=True, choices=ORDER_CHOICES)

    def __str__(self):
        return self.title