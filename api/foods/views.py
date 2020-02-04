from rest_framework import generics
from api.models import Food
from api.serializers import FoodSerializer


class FoodList(generics.ListCreateAPIView):
    """
    get:
    Get foods
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer