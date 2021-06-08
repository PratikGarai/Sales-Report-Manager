from django.urls import path
from .views import (
    home_view,
    SalesListView,
    SaleDetailView,
    UploadView,
    csv_upload_view
)

app_name = "sale"

urlpatterns = [
    path('', home_view, name ="home"),
    path('sales/', SalesListView.as_view(), name="list"),
    path('sale/<pk>/', SaleDetailView.as_view(), name="detail"),
    path('from_file/', UploadView.as_view(), name="from-file"),
    path('upload', csv_upload_view, name='upload')
]