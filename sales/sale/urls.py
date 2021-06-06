from django.urls import path
from .views import (
    home_view,
    SalesListView
)

app_name = "sale"

urlpatterns = [
    path('', home_view, name ="home"),
    path('list/', SalesListView.as_view(), name="list")
]
