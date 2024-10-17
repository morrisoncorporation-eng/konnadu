from django.db import models
from solo.models import SingletonModel
from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import SiteConfiguration

# config = SiteConfiguration.objects.get()
config = SiteConfiguration.get_solo()

admin.site.site_header = config.site_header
admin.site.site_title = config.site_title
admin.site.index_title = config.index_title

admin.site.register(SiteConfiguration, SingletonModelAdmin)



class SiteConfiguration(SingletonModel):
    site_title = models.CharField(max_length=255, default="Site Title")
    index_title = models.CharField(max_length=255, default="Site Name")
    site_header = models.CharField(max_length=255, default="Site Header")


    def __str__(self):
        return "Site Configuration."

    class Meta:
        verbose_name = "Site Configuration"