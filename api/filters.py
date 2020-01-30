import rest_framework_filters as filters
from api.models import FoodTable, FoodOrder, Food, Client, Sale


class FoodTableFilter(filters.FilterSet):
    class Meta:
        model = FoodTable
        fields = {'table_status_id': ['in']}


class FoodFilter(filters.FilterSet):
    class Meta:
        model = Food
        fields = {'name': ['icontains']}


class FoodOrderFilter(filters.FilterSet):
    food = filters.RelatedFilter(FoodFilter,
                                 field_name='food',
                                 queryset=Food.objects.all())

    class Meta:
        model = FoodOrder
        fields = {
            'order_status_id': ['in', 'exact'],
            'food_table_id': ['in', 'exact']
        }


class ClientFilter(filters.FilterSet):
    class Meta:
        model = Client
        fields = {'identifier': ['exact', 'in']}


class SaleFilter(filters.FilterSet):
    client = filters.RelatedFilter(ClientFilter,
                                   field_name='client',
                                   queryset=Client.objects.all())

    class Meta:
        model = Sale
        fields = {
            'sale_status_id': ['exact', 'in'],
            'sale_type_id': ['exact', 'in'],
            'code': ['exact', 'in'],
        }
