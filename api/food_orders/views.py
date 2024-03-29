from rest_framework import viewsets, status, generics, serializers
from rest_framework.response import Response
from api.serializers import ResponseFoodOrderSerializer, FoodOrderSerializer
from api.models import FoodOrder, Food
from api.filters import FoodOrderFilter
from api.paginators import TwentyResultsPaginator
from api.meta_data import OrderStatusID


class FoodOrderList(generics.ListAPIView):
    """
    get:

    Get paginated and filtered list of food_orders
    You can filter by:
    fields = {
            'order_status_id': ['in', 'exact'],
            'food_table_id': ['in', 'exact'],
            'created_at': ['gte', 'lte']
        }
    """
    queryset = FoodOrder.objects.all()
    serializer_class = FoodOrderSerializer
    filter_class = FoodOrderFilter
    pagination_class = TwentyResultsPaginator


class FoodDetail(generics.RetrieveUpdateDestroyAPIView):
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
        self.validate_food_order()
        return super(FoodDetail, self).update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        delete:
        Logic Delete Food Order by ID
        """
        self.validate_food_order()
        return super(FoodDetail, self).delete(request, *args, **kwargs)

    def validate_food_order(self):
        if self.get_object().sale_id is not None:
            raise serializers.ValidationError('Billed order.')
        elif not self.get_object().order_status_id == OrderStatusID.CREATED:
            raise serializers.ValidationError('Order must be in CREATED state')


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
        foods = Food.objects.filter(id__in=[food_order['food_id'] for food_order in data['food_orders']])
        foods_dicts = {
            int(food.id): food
        for food in foods}
        for food_order in data['food_orders']:
            food_order['food_table_id'] = food_table_id
            food_order['price'] = foods_dicts[int(food_order['food_id'])].price
            serializer = ResponseFoodOrderSerializer(data=food_order)
            serializer.is_valid(raise_exception=True)
            to_save.append(serializer)
        for save_obj in to_save:
            save_obj.save()
            response['food_orders'].append(save_obj.data)
        return Response(response, status=status.HTTP_201_CREATED)
