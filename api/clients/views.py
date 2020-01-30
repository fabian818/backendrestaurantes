from rest_framework import generics
from api.models import Client
from api.serializers import ClientSerializer
from api.filters import ClientFilter


class ClientList(generics.ListCreateAPIView):
    """
    get:
    Get clients
    post:
    Save client, body example:
    {
        'identifier': '72446953',
        'name': 'Alvarito',
        'last_name': 'Palacios Carrillo'
    }
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_class = ClientFilter