from rest_framework import generics
from api.models import Sale
from api.serializers import SaleSerializer
from api.paginators import FiftyResultsPaginator
# from api.filters import FoodTableFilter


class SaleList(generics.ListAPIView):
    """
    get:
    Get tables with sales,
    # You can filter by:
    # sale_status as follows: /api/food_tables/?sale_status_id__in=1
    # sale_types as follows: /api/food_tables/?sale_type_id__in=1
    # where the table_status_id must be: 1 (ready), 2 (occupied), 3 (deleted)
    """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    pagination_class = FiftyResultsPaginator
    # filter_class = FoodTableFilter
