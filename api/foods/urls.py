from django.urls import path
from api.foods.views import FoodList

urlpatterns = [path('', FoodList.as_view())]
