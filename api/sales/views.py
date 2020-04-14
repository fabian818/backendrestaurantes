from rest_framework import status, generics
from rest_framework.response import Response
from api.models import Sale, FoodOrder, SaleType
from api.serializers import SaleSerializer, CreateSaleSerializer
from api.paginators import TwentyResultsPaginator
from api.filters import SaleFilter
from django.forms.models import model_to_dict
from django.db.models import Sum
from api.meta_data import OrderStatusID, SaleStatusID


class SaleList(generics.ListCreateAPIView):
    """
    get:
    Get tables with sales,
    You can filter by:
    client__identifier as follows: /api/food_tables/?client__identifier=123123123
    code as follows: /api/food_tables/?code=123123123
    code__in as follows: /api/food_tables/?code__in=123123123,23423423434
    code__icontains as follows: /api/food_tables/?code__icontains=123
    sale_status_id as follows: /api/food_tables/?sale_status_id=1
    sale_status_id__in as follows: /api/food_tables/?sale_status_id__in=1,2,3
    sale_type_id as follows: /api/food_tables/?sale_type_id=1
    sale_type_id__in as follows: /api/food_tables/?sale_type_id__in=1,2,3
    created_at as follows: /api/food_tables/?created_at__gte=2020-02-03&created_at__lte=2020-03-10
    where the sale_status_id must be: 1 (created), 2 (paid), 3 (deleted), 4 (canceled)
    where the sale_type_id must be: 1 (boleta), 2 (factura)
    """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    pagination_class = TwentyResultsPaginator
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
        status_dict = {
            SaleStatusID.CREATED: OrderStatusID.RELATED,
            SaleStatusID.PAID: OrderStatusID.PAID
        }
        food_orders.update(
            sale_id=serializer.data['id'],
            order_status_id=status_dict.get(serializer.data['sale_status_id'])
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SalesDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    patch: parcial update for sale
    """
    queryset = Sale.objects.all()
    serializer_class = CreateSaleSerializer

