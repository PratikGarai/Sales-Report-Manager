from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
import pandas as pd

def home_view(request):
    form = SalesSearchForm(request.POST or None)
    sale_df = None
    if request.method=='POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')

        qs = Sale.objects.filter(created__gte=date_from, created__lte=date_to)
        if len(qs)>0:
            sale_df = pd.DataFrame(qs.values())
            print(sale_df)
            sale_df = sale_df.to_html()
        else :
            print('No sale data for the date query')

    context = {
        'form' : form,
        'sales_df' : sale_df
    }
    return render(request, "sale/home.html", context)

class SalesListView(ListView):
    model = Sale
    template_name = "sale/main.html"

class SaleDetailView(DetailView):
    model = Sale
    template_name = "sale/detail.html"