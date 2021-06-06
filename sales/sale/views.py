from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale

def home_view(request):
    return render(request, "sale/main.html", {})


class SalesListView(ListView):
    model = Sale
    template_name = "sale/main.html"

class SaleDetailView(DetailView):
    model = Sale
    template_name = "sale/detail.html"