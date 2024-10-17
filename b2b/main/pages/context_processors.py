from .models import Page


def get_inner_categories(requst):
    popular = Page.objects.all().order_by("-popularity")[:6]
    included = popular.values_list("id", flat=True)
    categories = Page.objects.exclude(id__in=included)
    return {"popular": popular, "categories": categories}
