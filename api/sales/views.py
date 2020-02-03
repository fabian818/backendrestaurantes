from rest_framework import status, generics
from rest_framework.response import Response
from api.models import Sale, FoodOrder, SaleType
from api.serializers import SaleSerializer, CreateSaleSerializer
from api.paginators import FiftyResultsPaginator
from api.filters import SaleFilter
from django.forms.models import model_to_dict
from django.db.models import Sum


class SaleList(generics.ListCreateAPIView):
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

    def create(self, request):
        """
        Method for create a Sale
        """
        data = request.data
        food_orders = FoodOrder.objects.filter(id__in=data['food_orders'])
        data['total'] = food_orders.aggregate(sum_total=Sum('total'))['sum_total']
        serializer = CreateSaleSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        food_orders.update(sale_id=serializer.data['id'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)
