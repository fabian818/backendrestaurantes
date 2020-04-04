from rest_framework import status, generics
from rest_framework.response import Response
from api.models import FoodCategory, Food
from api.serializers import FoodCategorySerializer, FoodSerializer
from api.filters import FoodCategoryFilter, FoodFilter
from api.paginators import FiftyResultsPaginator
from slugify import slugify


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

    def create(self, request):
        data = request.data
        data['name'] = slugify(data['display_name'])
        serializer = FoodCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



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
