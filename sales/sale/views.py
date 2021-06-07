from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
import pandas as pd
from .utils import get_customer_from_id, get_salesman_from_id, get_chart
from report.forms import ReportForm


def home_view(request):
    sale_df = None
    pos_df = None
    merged_df = None
    chart = None
    searchForm = SalesSearchForm(request.POST or None)
    reportForm = ReportForm()

    if request.method=='POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        qs = Sale.objects.filter(created__gte=date_from, created__lte=date_to)

        if len(qs)>0:
            sale_df = pd.DataFrame(qs.values())
            sale_df['customer_id'] = sale_df['customer_id']\
                                    .apply(get_customer_from_id)\
                                    .apply(lambda x : x.name)
            sale_df['salesman_id'] = sale_df['salesman_id']\
                                    .apply(get_salesman_from_id)\
                                    .apply(lambda x : x.user.username)
            sale_df.rename({
                'id' : 'sales_id',
                'customer_id' : 'customer', 
                'salesman_id' : 'salesman'
            }, axis=1, inplace=True)
            positions_data = []

            for sale in qs :
                for pos in sale.get_positions():
                    obj = {
                        'sales_id' : pos.get_sales_id(),
                        'position_id' : pos.id,
                        'product' : pos.product.name,
                        'quantity' : pos.quantity,
                        'price' : pos.price
                    }
                    positions_data.append(obj)

            pos_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sale_df, pos_df, on='sales_id')
            chart = get_chart(chart_type, sale_df, labels=sale_df['transaction_id'].values)

            pos_df = pos_df.to_html()
            sale_df = sale_df.to_html()
            merged_df = merged_df.to_html()
        else :
            print('No sale data for the date query')

    context = {
        'search_form' : searchForm,
        'sales_df' : sale_df,
        'pos_df' : pos_df,
        'merge_df' : merged_df,
        'chart' : chart,
        'report_form' : reportForm
    }
    return render(request, "sale/home.html", context)


class SalesListView(ListView):
    model = Sale
    template_name = "sale/main.html"


class SaleDetailView(DetailView):
    model = Sale
    template_name = "sale/detail.html"