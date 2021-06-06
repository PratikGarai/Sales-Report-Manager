from django.shortcuts import render
from django.views.generic import ListView
from .models import Sale

def home_view(request):
    return render(request, "sale/main.html", {})


class SalesListView(ListView):
    model = Sale
    template_name = "sale/main.html"