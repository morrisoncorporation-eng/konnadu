from django.views.generic import ListView
from .models import Store

class MarketListView(ListView):
    template_name = "market/index.html"
    model = Store
    paginate_by = 50