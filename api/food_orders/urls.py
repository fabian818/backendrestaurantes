from django.urls import path
from api.food_orders.views import FoodOrdersViewSet, FoodOrderList

urlpatterns = [
    path('bulk_create/', FoodOrdersViewSet.as_view({'post': 'bulk_create'})),
    path('', FoodOrderList.as_view()),
]
