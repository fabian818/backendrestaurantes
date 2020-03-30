from django.urls import path, include

urlpatterns = [
    path('food_tables/', include('api.food_tables.urls')),
    path('food_orders/', include('api.food_orders.urls')),
    path('sales/', include('api.sales.urls')),
    path('clients/', include('api.clients.urls')),
    path('foods/', include('api.foods.urls')),
    path('admin/', include('api.api_admin.urls')),
]
