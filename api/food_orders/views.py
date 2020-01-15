from rest_framework import viewsets
from rest_framework.response import Response


class FoodOrdersViewSet(viewsets.ViewSet):
    def bulk_create(self, *args, **kwargs):
        return Response({'message': 'success'}, status=201)
