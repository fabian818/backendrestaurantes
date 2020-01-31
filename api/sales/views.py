from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from api.models import Sale, FoodOrder, SaleType
from api.serializers import SaleSerializer, CreateSaleSerializer
from api.paginators import FiftyResultsPaginator
from api.filters import SaleFilter
from django.forms.models import model_to_dict


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
        response = {
            'code': None,
            'client': None,
            'total': None,
            'payment': data['payment'],
            'change': None,
            'food_orders': [],
            'sale_status': None,
            'sale_type': None
        }
        food_orders = []
        total = 0
        for food_order_id in data['food_orders']:
            food_order = FoodOrder.objects.get(pk=food_order_id)
            food_orders.append(food_order)
            total += food_order.total

        data['total'] = total
        serializer = CreateSaleSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        sale = serializer.save()

        orders_serialized = []
        for food_order in food_orders:
            food_order.sale_id = sale.id
            food_order.save()
            order_serialized = model_to_dict(food_order)
            orders_serialized.append(order_serialized)

        client_serialized = model_to_dict(sale.client)
        sale_type = SaleType.objects.get(pk=data['sale_type_id'])
        response['client'] = client_serialized
        response['code'] = sale.code
        response['total'] = sale.total
        response['change'] = sale.change
        response['food_orders'] = orders_serialized
        response['sale_status'] = model_to_dict(sale.sale_status)
        response['sale_type'] = model_to_dict(sale_type)

        return Response(response, status=status.HTTP_201_CREATED)
