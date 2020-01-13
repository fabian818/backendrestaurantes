from rest_framework import generics
from api.models import FoodTable
from api.serializers import FoodTableSerializer


class FoodTableList(generics.ListAPIView):
    """
    get:
    Get tables with orders
    """
    queryset = FoodTable.objects.all()
    serializer_class = FoodTableSerializer


class FoodTableDetail(generics.RetrieveAPIView):
    """
    get:
    Get table with a ID
    """
    queryset = FoodTable.objects.all()
    serializer_class = FoodTableSerializer