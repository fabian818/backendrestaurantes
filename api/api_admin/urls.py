from django.urls import path
from api.api_admin.views import FoodCategoriesList

urlpatterns = [path('food_categories', FoodCategoriesList.as_view())]
