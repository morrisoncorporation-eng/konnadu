from django.contrib import admin
from solo.admin import SingletonModelAdmin
from main.market.models import Store, Image, HowTo
from main.pages.models import Page, Jumbotron
from main.customer.models import Customer
from main.order.models import Order
from main.cart.models import Cart
from main.address.models import Address
from main.shipping.models import Shipping
from main.site_settings.models import SiteConfiguration


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("customer", "default", "state", "country", "address",)
    list_filter = ("customer", "address",)
    search_fields = ("customer__user__username", "address", "country")

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    pass

@admin.register(Jumbotron)
class JumbotronAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass

class ImageInline(admin.StackedInline):
    model = Image
    extra = 0
    max_num = 1

class HowToInline(admin.StackedInline):
    model = HowTo
    extra = 1

@admin.action(description='Mark selected stores as popular')
def mark_popular(modeladmin, request, queryset):
    queryset.update(popular=True)

@admin.action(description='Mark selected stores as exclusive')
def mark_exclusive(modeladmin, request, queryset):
    queryset.update(is_exclusive=True)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    inlines = (ImageInline, HowToInline)
    prepopulated_fields = {"slug":("name",)}
    actions = [mark_popular, mark_exclusive]



@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title",)}

class CartInline(admin.StackedInline):
    model = Cart
    extra = 0
    readonly_fields = ('title', 'image', 'owner', 'shop_name', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "status", "order_id", "created_date")
    readonly_fields = ("order_id",)
    inlines = (CartInline,)





# config = SiteConfiguration.objects.get()
config = SiteConfiguration.get_solo()


admin.site.site_header = config.site_name
# admin.site.site_title = config.site_title
# admin.site.index_title = config.index_title

admin.site.register(SiteConfiguration, SingletonModelAdmin)
