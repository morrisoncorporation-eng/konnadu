from django.urls import path
from . import views
app_name = "market"

urlpatterns = [
    path("home/", views.MarketListView.as_view(), name="market_list")
]
