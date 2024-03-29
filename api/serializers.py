from rest_framework import serializers
from api.models import FoodTable, FoodOrder, Food, Sale, Client, SaleStatus, FoodCategory, HistoricalPrice
from api.meta_data import OrderStatusID


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class HistoricalPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPrice
        fields = '__all__'


class FoodOrderSerializer(serializers.ModelSerializer):
    food = FoodSerializer(required=False)
    food_id = serializers.IntegerField(allow_null=False)
    food_table_id = serializers.IntegerField(allow_null=False)

    class Meta:
        model = FoodOrder
        exclude = ('food_table', )


class FoodTableSerializer(serializers.ModelSerializer):
    identifier = serializers.CharField(read_only=True)
    food_orders = serializers.SerializerMethodField(source='food_orders',
                                                    read_only=True)

    class Meta:
        model = FoodTable
        child = FoodOrder
        fields = '__all__'

    @staticmethod
    def get_food_orders(obj):
        return FoodOrderSerializer(
            obj.food_orders.filter(order_status_id__in=[OrderStatusID.CREATED, OrderStatusID.RELATED]),
            many=True,
            read_only=True).data


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class FoodCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = FoodCategory
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    food_orders = FoodOrderSerializer(many=True, read_only=True)
    class Meta:
        model = Sale
        fields = '__all__'


class ResponseFoodOrderSerializer(serializers.ModelSerializer):
    food = FoodSerializer(required=False)
    sale = SaleSerializer(required=False)
    food_id = serializers.IntegerField(allow_null=False)
    food_table_id = serializers.IntegerField(allow_null=False)
    food_table = FoodTableSerializer(required=False)
    total = serializers.FloatField(required=False)
    order_status_id = serializers.IntegerField(allow_null=False,
                                               required=False)
    price = serializers.FloatField(required=False)

    class Meta:
        model = FoodOrder
        fields = '__all__'


class SaleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleStatus
        fields = '__all__'


class CreateSaleSerializer(serializers.ModelSerializer):
    client = ClientSerializer(required=False)
    client_id = serializers.IntegerField(allow_null=False)
    code = serializers.CharField(required=False)
    change = serializers.FloatField(required=False)
    payment = serializers.FloatField(required=False)
    sale_type_id = serializers.IntegerField(allow_null=False, required=False)
    sale_status_id = serializers.IntegerField(allow_null=False, required=False)
    total = serializers.FloatField(required=False)
    sale_status = SaleStatusSerializer(required=False, read_only=True)

    class Meta:
        model = Sale
        fields = '__all__'
