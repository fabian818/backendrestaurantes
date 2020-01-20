from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from api.serializers import ResponseFoodOrderSerializer, FoodOrderSerializer
from api.models import FoodOrder
from api.filters import FoodOrderFilter


class FoodOrderList(generics.ListAPIView):
    """
    get:

    Get paginated and filtered list of food_orders
    """
    queryset = FoodOrder.objects.all()
    serializer_class = FoodOrderSerializer
    filter_class = FoodOrderFilter


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
