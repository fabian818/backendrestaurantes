from django.urls import path
from api.sales.views import SaleList, SalesDetail

urlpatterns = [
    path('', SaleList.as_view()),
    path('<int:pk>/', SalesDetail.as_view())
]
