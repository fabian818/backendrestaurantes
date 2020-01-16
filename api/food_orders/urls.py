from django.urls import path
from api.food_orders.views import FoodOrdersViewSet

urlpatterns = [
    path('bulk_create/', FoodOrdersViewSet.as_view({'post': 'bulk_create'})),
]
