from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    # path("pages/", views.PageView.as_view(), name="pages"),
    path("", views.pages, name="page"),
    path("search/", views.search_view, name="search"),
    path("trending/", views.get_store_grouping, name="get-group"),
    path("category/", views.get_category, name="category"),
    path("more/", views.get_more, name="more"),
    path("download/", views.download_plugin, name="download"),
]