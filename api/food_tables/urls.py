from django.urls import path
from api.food_tables.views import FoodTableList


urlpatterns = [
    path('', FoodTableList.as_view()),
]
