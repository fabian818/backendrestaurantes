from rest_framework import generics
from api.models import Client
from api.serializers import ClientSerializer
from api.filters import ClientFilter


class ClientList(generics.ListAPIView):
    """
    get:
    Get clients
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_class = ClientFilter