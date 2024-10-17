from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from .models import Page, Jumbotron
from main.market.models import Store


def pages(request):
    jumbo_one = Jumbotron.objects.filter(order=1).first()
    jumbo_two = Jumbotron.objects.filter(order=2).first()
    jumbo_three = Jumbotron.objects.filter(order=3).first()
    popular = Store.objects.filter(popular=True)[:4]
    exclusive = Store.objects.filter(is_exclusive=True)[:12]
    stores = Store.objects.all()[:12]
    object_list = Page.objects.all()

    ctx = {
        "jumbo_one": jumbo_one,
        "jumbo_two": jumbo_two,
        "jumbo_three": jumbo_three,
        "object_list": object_list,
        "popular": popular,
        "exclusive": exclusive,
        "stores": stores,
    }
    return render(request, "pages/page.html", ctx)


def get_store_grouping(request):
    if request.htmx:
        stores_list = Store.objects.all()
        paginator = Paginator(stores_list, 25)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "pages/partials/_replacement.html", {"stores": page_obj})


def get_category(request):
    if request.htmx:
        if request.GET.get("exclusive"):
            category_name = "exclusive"
            is_exclusive = Store.objects.filter(is_exclusive=True).order_by("-id")
            paginator = Paginator(is_exclusive, 12)
            page_number = request.GET.get("page")
            stores = paginator.get_page(page_number)
        if request.GET.get("trending"):
            category_name = "trending"
            trending = Store.objects.all().order_by("-id")
            paginator = Paginator(trending, 12)
            page_number = request.GET.get("page")
            stores = paginator.get_page(page_number)
        if request.GET.get("category-id"):
            page = Page.objects.get(id=request.GET.get("category-id"))
            category_name = page.title
            stores = page.store.all()
        return render(
            request,
            "pages/partials/_category.html",
            {
                "stores": stores,
                "category_name": category_name,
            },
        )


def get_more(request):
    has_page = True
    if request.htmx:
        page_counter = 1
        from_request = int(request.GET.get("page"))
        page_number = page_counter + from_request
        category_name = request.GET.get("category-name")
        if category_name == "trending":
            p = Store.objects.all().order_by("-id")
            try:
                stores = Paginator(p, 12)
                page = stores.page(page_number)
                object_list = page.object_list
                return render(
                    request,
                    "pages/partials/_more.html",
                    {"stores": object_list, "has_page": has_page},
                )
            except EmptyPage:
                has_page = False
                object_list = []
                return render(
                    request,
                    "pages/partials/_more.html",
                    {"stores": object_list, "has_page": has_page},
                )
        if category_name == "exclusive":
            p = Store.objects.filter(is_exclusive=True).order_by("-name")
            try:
                stores = Paginator(p, 12)
                page = stores.page(page_number)
                object_list = page.object_list
                return render(
                    request,
                    "pages/partials/_more.html",
                    {"stores": object_list, "has_page": has_page},
                )
            except EmptyPage:
                has_page = False
                object_list = []
                return render(
                    request,
                    "pages/partials/_more.html",
                    {"stores": object_list, "has_page": has_page},
                )
        if category_name:
            page = Page.objects.filter(title=category_name.lower()).first()
            p = page.store.all().order_by("-name")
            try:
                stores = Paginator(p, 12)
                page = stores.page(page_number)
                object_list = page.object_list
                return render(
                    request,
                    "pages/partials/_more.html",
                    {"stores": object_list, "has_page": has_page},
                )
            except EmptyPage:
                has_page = False
                object_list = []
                return render(
                    request,
                    "pages/partials/_more.html",
                    {"stores": object_list, "has_page": has_page},
                )
    return render(
        request,
        "pages/partials/_more.html",
        {"stores": [], "has_page": False},
    )


def search_view(request):
    if request.htmx:
        q = request.GET.get("q")
        stores = Store.objects.filter(name__icontains=q).order_by("name")
        paginator = Paginator(stores, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    return render(request, "pages/partials/_search_result.html", {"result": page_obj})


def download_plugin(request):
    is_mobile = request.user_agent.is_mobile
    disabled = ""
    if is_mobile:
        disabled = "disabled"
    else:
        browser = request.user_agent.browser.family
        url = ""
    return render(
        request,
        "pages/download.html",
        {"browser": browser, "disabled": disabled, "url": url},
    )
