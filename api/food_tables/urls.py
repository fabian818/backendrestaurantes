from django.urls import path
from api.food_tables.views import FoodTableList, FoodTableDetail

urlpatterns = [
    path('', FoodTableList.as_view()),
    path('<int:pk>', FoodTableDetail.as_view()),
]
