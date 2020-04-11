from rest_framework import generics, status
from rest_framework.response import Response
from api.models import FoodCategory, Food, HistoricalPrice, FoodTable, FoodOrder
from api.serializers import FoodCategorySerializer, FoodSerializer, HistoricalPriceSerializer, FoodTableSerializer
from api.filters import FoodCategoryFilter, FoodFilter, HistoricalPriceFilter, FoodTableFilter
from api.paginators import FiftyResultsPaginator
from api.meta_data import OrderStatusID


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
    Filter by:
    table_status_id__in 1, 2, 3
    display_name__in
    display_name__exact
    display_name__icontains
    """
    queryset = FoodTable.objects.all()
    serializer_class = FoodTableSerializer
    filter_class = FoodTableFilter
    pagination_class = FiftyResultsPaginator


class FoodTablesDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    patch:
    Parcial update for food tables
    """
    queryset = FoodTable.objects.all()
    serializer_class = FoodTableSerializer

    def delete(self, request, *args, **kwargs):
        """
        Method for soft delete a Food Table
        """
        if self.validate_food_table():
            return super(FoodTablesDetail,
                         self).delete(request, *args, **kwargs)
        else:
            return Response(
                data={"message": "Food Table has orders created o relateds!"},
                status=status.HTTP_400_BAD_REQUEST)


    def validate_food_table(self):
        food_table_id = self.get_object().id
        created_orders = FoodOrder.objects.filter(
            food_table_id=food_table_id, order_status=OrderStatusID.CREATED)
        related_orders = FoodOrder.objects.filter(
            food_table_id=food_table_id, order_status=OrderStatusID.RELATED)
        return created_orders.count() == 0 and related_orders.count() == 0
