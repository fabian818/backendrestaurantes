from rest_framework import viewsets
import rest_framework_filters as filters
from api.models import FoodTable, FoodOrder, Food


class FoodTableFilter(filters.FilterSet):
    class Meta:
        model = FoodTable
        fields = {'table_status_id': ['in']}


class FoodFilter(filters.FilterSet):
    class Meta:
        model = Food
        fields = {
            'name': ['icontains']
        }


class FoodOrderFilter(filters.FilterSet):
    food = filters.RelatedFilter(FoodFilter, field_name='food', queryset=Food.objects.all())

    class Meta:
        model = FoodOrder
        fields = {
            'order_status_id': ['in', 'exact'],
            'food_table_id': ['in', 'exact']
        }
