from django.urls import path, include


urlpatterns = [
    path('food_tables/', include('api.food_tables.urls')),
]
