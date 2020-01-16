from rest_framework import viewsets
import rest_framework_filters as filters
from api.models import FoodTable


class FoodTableFilter(filters.FilterSet):
    class Meta:
        model = FoodTable
        fields = {'table_status_id': ['in']}