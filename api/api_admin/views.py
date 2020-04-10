from rest_framework import generics
from api.models import FoodCategory, Food, HistoricalPrice, FoodTable
from api.serializers import FoodCategorySerializer, FoodSerializer, HistoricalPriceSerializer, FoodTableSerializer
from api.filters import FoodCategoryFilter, FoodFilter, HistoricalPriceFilter
from api.paginators import FiftyResultsPaginator


class HistoricalPricesList(generics.ListAPIView):
    """
    get:
    Get historical prices
    Filter:
    By food_id in or exact
    """
    queryset = HistoricalPrice.objects.all()
    serializer_class = HistoricalPriceSerializer
    filter_class = HistoricalPriceFilter
    pagination_class = FiftyResultsPaginator


class FoodCategoriesList(generics.ListCreateAPIView):
    """
    get:
    Get food categories
    post:
    Save food category, body example:
    {
        'display_name': 'Desayuno',
        'description': 'Descripción del desayuno'
    }
    """
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    filter_class = FoodCategoryFilter
    pagination_class = FiftyResultsPaginator


class FoodsList(generics.ListCreateAPIView):
    """
    get:
    Get foods
    post:
    Save foods, body example:
    {
        'food_status_id': 1,
        'food_category_id': 1,
        'name': 'Ají de Gallina',
        'price': 10.00
    }
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    filter_class = FoodFilter
    pagination_class = FiftyResultsPaginator


class FoodCategoriesDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    patch:
    Parcial update for food_category
    """
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer


class FoodsDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    patch:
    Parcial update for food
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class FoodTablesList(generics.ListCreateAPIView):
    """
    get:
    Get food tables
    post:
    Save food tables, body example:
    {
        'display_name': 'Mesa 1',
        'description': 'Descripción de la mesa'
    }
    """
    queryset = FoodTable.objects.all()
    serializer_class = FoodTableSerializer


class FoodTablesDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    patch:
    Parcial update for food tables
    """
    queryset = FoodTable.objects.all()
    serializer_class = FoodTableSerializer