from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Image(models.Model):
    store = models.ForeignKey("Store", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="shop/")
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name

    class Meta:
        db_table = "images"


class HowTo(models.Model):
    content = models.TextField()
    step = models.IntegerField()
    image = models.ImageField(upload_to="shop/howto")
    video_url = models.URLField(blank=True, max_length=255)
    store = models.ForeignKey(
        "Store",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="how_to_store",
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Step-> {self.step} Store: {self.store.name}'

    class Meta:
        ordering = ('step',)


class Store(models.Model):
    """
    This model serves as main store front objects.
    Example a samsung shop has a name, an Image
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    url = models.URLField()
    trending = models.BooleanField(default=False)
    popular = models.BooleanField(default=False)
    is_exclusive = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "store"

    @property
    def get_first_image(self):
        images = self.image_set.all()
        if images:
            return images.first().image.url
        else:
            return
