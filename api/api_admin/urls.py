from django.urls import path
from api.api_admin.views import FoodCategoriesList, FoodsList

urlpatterns = [
    path('food_categories', FoodCategoriesList.as_view()),
    path('foods', FoodsList.as_view()),
]
