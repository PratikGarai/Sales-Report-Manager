from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Sale
from .forms import SalesSearchForm
from .utils import get_customer_from_id, get_salesman_from_id, get_chart
from report.forms import ReportForm
from .models import Sale, CSV, Position
from products.models import Product
from customers.models import Customer
from profiles.models import Profile

import pandas as pd
import csv


@login_required
def home_view(request):
    sale_df = None
    pos_df = None
    merged_df = None
    chart = None
    searchForm = SalesSearchForm(request.POST or None)
    reportForm = ReportForm()
    no_data = False

    if request.method=='POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')
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
            chart = get_chart(chart_type, sale_df, results_by)

            pos_df = pos_df.to_html()
            sale_df = sale_df.to_html()
            merged_df = merged_df.to_html()
        else :
            no_data = True
            print('No sale data for the date query')

    context = {
        'search_form' : searchForm,
        'sales_df' : sale_df,
        'pos_df' : pos_df,
        'merge_df' : merged_df,
        'chart' : chart,
        'report_form' : reportForm,
        'no_data' : no_data
    }
    return render(request, "sale/home.html", context)


class SalesListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = "sale/main.html"


class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = "sale/detail.html"


class UploadView(LoginRequiredMixin, TemplateView):
    template_name = "sale/from_file.html"


@login_required
def csv_upload_view(request):
    if request.method=="POST":
        csv_file = request.FILES.get('file')
        obj = CSV.objects.create(file_name=csv_file)

        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader :
                transaction_id = row[1]
                product = row[2]
                quantity = int(row[3])
                customer = row[4]
                date = row[5].split('-')
                date = "-".join(date[::-1])
                date = parse_date(date)

                try :
                    product_obj = Product.objects.get(name__iexact = product)
                except :
                    product_obj = None
                    print(f"Product {product} does not exist")
                
                if product_obj : 
                    customer_obj, _ = Customer.objects.get_or_create(name=customer)
                    salesman_obj = Profile.objects.get(user=request.user)
                    position_obj = Position.objects.create(product=product_obj, \
                                    quantity=quantity, created=date)

                    sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, \
                                customer=customer_obj, salesman=salesman_obj, created=date)
                    sale_obj.positions.add(position_obj)
                    sale_obj.save()


    return HttpResponse("CSV upload view")