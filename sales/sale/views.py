from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm

def home_view(request):
    form = SalesSearchForm(request.POST or None)
    context = {
        'form' : form
    }
    return render(request, "sale/home.html", context)

class SalesListView(ListView):
    model = Sale
    template_name = "sale/main.html"

class SaleDetailView(DetailView):
    model = Sale
    template_name = "sale/detail.html"