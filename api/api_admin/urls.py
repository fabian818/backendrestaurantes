from django.urls import path
from api.api_admin.views import FoodCategoriesList, FoodsList, FoodCategoriesDetail

urlpatterns = [
    path('food_categories', FoodCategoriesList.as_view()),
    path('foods', FoodsList.as_view()),
    path('food_categories/<int:pk>/', FoodCategoriesDetail.as_view())
]
