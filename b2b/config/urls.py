"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("main.pages.urls", namespace="pages")),
    path("home/", include("main.homepage.urls", namespace="homepage")),
    path("market/", include("main.market.urls", namespace="market")),
    path("customer/", include("main.customer.urls", namespace="customer")),
    path("dashboard/", include("main.dashboard.urls", namespace="dashboard")),
    path("address/", include("main.address.urls", namespace="address")),
    path("shipping/", include("main.shipping.urls", namespace="shipping")),
    path("payment/", include("main.payment.urls", namespace="payment")),
    path("order/", include("main.order.urls", namespace="order")),
    path("cart/", include("main.cart.urls", namespace="cart")),
    path("accounts/", include("allauth.urls")),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path("pages/", include("django.contrib.flatpages.urls")),
    path("tinymce/", include("tinymce.urls")),
    path("admin/", admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
