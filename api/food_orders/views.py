from rest_framework import viewsets, status, generics, serializers
from rest_framework.response import Response
from django.forms.models import model_to_dict
from api.serializers import ResponseFoodOrderSerializer, FoodOrderSerializer
from api.models import FoodOrder
from api.filters import FoodOrderFilter
from api.paginators import FiftyResultsPaginator
from api.meta_data import OrderStatusID


class FoodOrderList(generics.ListAPIView):
    """
    get:

    Get paginated and filtered list of food_orders
    """
    queryset = FoodOrder.objects.all()
    serializer_class = FoodOrderSerializer
    filter_class = FoodOrderFilter
    pagination_class = FiftyResultsPaginator


class FoodUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    put:
    Update Food Order by ID
    Example Body:
    {
        "price": 20.00,
        "quantity": 10,
        "food_id": 1,
        "food_table_id": 1
    }
    """
    queryset = FoodOrder.objects.all()
    serializer_class = ResponseFoodOrderSerializer

    def update(self, request, *args, **kwargs):
        if self.get_object().sale_id is not None:
            raise serializers.ValidationError('Billed order.')
        elif not self.get_object().order_status_id == OrderStatusID.CREATED:
            raise serializers.ValidationError('Order must be in CREATED state')
        return super(FoodUpdateDelete, self).update(request, *args, **kwargs)

    def delete(self, request, pk):
        """
        delete:
        Logic Delete Food Order by ID
        """
        food_order = self.get_object()

        if food_order.sale_id is not None:
            raise serializers.ValidationError('Billed order.')
        elif not food_order.order_status_id == OrderStatusID.CREATED:
            raise serializers.ValidationError('Order must be in CREATED state')

        food_order.order_status_id = OrderStatusID.DELETED
        food_order.save()

        food_order = model_to_dict(food_order)
        return Response(food_order, status=status.HTTP_200_OK)


class FoodOrdersViewSet(viewsets.ViewSet):
    def bulk_create(self, *args, **kwargs):
        """
        Method for create a list of food_orders
        """

        data = self.request.data
        food_table_id = data['food_table_id']
        response = {
            'food_table_id': food_table_id,
            'food_orders': []
        }
        to_save = []
        for food_order in data['food_orders']:
            food_order['food_table_id'] = food_table_id
            serializer = ResponseFoodOrderSerializer(data=food_order)
            serializer.is_valid(raise_exception=True)
            to_save.append(serializer)
        for save_obj in to_save:
            save_obj.save()
            response['food_orders'].append(save_obj.data)
        return Response(response, status=status.HTTP_201_CREATED)
