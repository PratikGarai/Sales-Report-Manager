from django.urls import path
from .views import (
    create_report_view, 
    ReportListView, 
    ReportDetailView
)

app_name = 'report'

urlpatterns = [
    path('save/', create_report_view, name='create-report'),
    path('', ReportListView.as_view() , name='list'),
    path('<pk>/', ReportDetailView.as_view() , name='detail')
]
