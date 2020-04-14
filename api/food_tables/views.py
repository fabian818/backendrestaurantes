from rest_framework import generics
from api.models import FoodTable
from api.serializers import FoodTableSerializer
from api.paginators import TwentyResultsPaginator
from api.filters import FoodTableFilter


class FoodTableList(generics.ListAPIView):
    """
    get:
    Get tables with orders,
    You can filter by table status as follows: /api/food_tables/?table_status_id__in=1
    where the table_status_id must be: 1 (ready), 2 (occupied), 3 (deleted)
    """
    queryset = FoodTable.objects.all()
    serializer_class = FoodTableSerializer
    filter_class = FoodTableFilter
    pagination_class = TwentyResultsPaginator


class FoodTableDetail(generics.RetrieveAPIView):
    """
    get:
    Get table by ID
    """
    queryset = FoodTable.objects.all()
    serializer_class = FoodTableSerializer
