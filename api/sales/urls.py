from django.urls import path
from api.sales.views import SaleList

urlpatterns = [
    path('', SaleList.as_view())
]
