from rest_framework import generics
from api.models import Food
from api.serializers import FoodSerializer
from api.paginators import TwentyResultsPaginator


class FoodList(generics.ListCreateAPIView):
    """
    get:
    Get foods
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    pagination_class = TwentyResultsPaginator
