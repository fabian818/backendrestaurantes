from django.urls import path
from api.api_admin.views import FoodCategoriesList, FoodsList, FoodCategoriesDetail, FoodsDetail, HistoricalPricesList, FoodTablesList, FoodTablesDetail

urlpatterns = [
    path('food_categories', FoodCategoriesList.as_view()),
    path('foods', FoodsList.as_view()),
    path('food_categories/<int:pk>/', FoodCategoriesDetail.as_view()),
    path('foods/<int:pk>/', FoodsDetail.as_view()),
    path('historical_prices', HistoricalPricesList.as_view()),
    path('food_tables', FoodTablesList.as_view()),
    path('food_tables/<int:pk>/', FoodTablesDetail.as_view()),
]
