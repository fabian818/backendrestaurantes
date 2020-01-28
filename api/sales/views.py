from rest_framework import generics
from api.models import Sale
from api.serializers import SaleSerializer
from api.paginators import FiftyResultsPaginator
from api.filters import SaleFilter


class SaleList(generics.ListAPIView):
    """
    get:
    Get tables with sales,
    You can filter by:
    client__identifier as follows: /api/food_tables/?client__identifier=123123123
    code as follows: /api/food_tables/?code=123123123
    sale_status as follows: /api/food_tables/?sale_status_id=1
    sale_types as follows: /api/food_tables/?sale_type_id=1
    where the sale_status_id must be: 1 (paid), 2 (deleted), 3 (canceled)
    where the sale_type_id must be: 1 (boleta), 2 (factura)
    """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    pagination_class = FiftyResultsPaginator
    filter_class = SaleFilter
