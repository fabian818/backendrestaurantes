from rest_framework import generics
from api.models import FoodCategory
from api.serializers import FoodCategorySerializer
from api.filters import FoodCategoryFilter
from api.paginators import FiftyResultsPaginator


class FoodCategoriesList(generics.ListCreateAPIView):
    """
    get:
    Get food categories
    post:
    Save food category, body example:
    {
        'name': 'Tamales',
        'display_name': 'Desayuno',
        'description': 'Descripción del desayuno'
    }
    """
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer
    filter_class = FoodCategoryFilter
    pagination_class = FiftyResultsPaginator