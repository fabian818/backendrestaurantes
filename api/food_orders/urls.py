from django.urls import path
from api.food_orders.views import FoodOrdersViewSet, FoodOrderList, FoodUpdateDelete

urlpatterns = [
    path('bulk_create/', FoodOrdersViewSet.as_view({'post': 'bulk_create'})),
    path('', FoodOrderList.as_view()),
    path('<int:pk>', FoodUpdateDelete.as_view()),
]
