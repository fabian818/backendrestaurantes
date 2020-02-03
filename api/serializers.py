from rest_framework import serializers
from api.models import FoodTable, FoodOrder, Food, Sale, Client, SaleStatus
from api.meta_data import OrderStatusID


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class FoodOrderSerializer(serializers.ModelSerializer):
    food = FoodSerializer(required=False)
    food_id = serializers.IntegerField(allow_null=False)
    food_table_id = serializers.IntegerField(allow_null=False)

    class Meta:
        model = FoodOrder
        exclude = ('food_table', )


class FoodTableSerializer(serializers.ModelSerializer):
    food_orders = serializers.SerializerMethodField(source='food_orders',
                                                    read_only=True)

    class Meta:
        model = FoodTable
        child = FoodOrder
        fields = '__all__'

    @staticmethod
    def get_food_orders(obj):
        return FoodOrderSerializer(
            obj.food_orders.filter(order_status_id=OrderStatusID.CREATED),
            many=True,
            read_only=True).data


class ResponseFoodOrderSerializer(serializers.ModelSerializer):
    food = FoodSerializer(required=False)
    food_id = serializers.IntegerField(allow_null=False)
    food_table_id = serializers.IntegerField(allow_null=False)
    food_table = FoodTableSerializer(required=False)
    total = serializers.FloatField(required=False)
    order_status_id = serializers.IntegerField(allow_null=False,
                                               required=False)

    class Meta:
        model = FoodOrder
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class SaleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleStatus
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = Sale
        fields = '__all__'


class CreateSaleSerializer(serializers.ModelSerializer):
    client = ClientSerializer(required=False)
    client_id = serializers.IntegerField(allow_null=False)
    code = serializers.CharField(required=False)
    change = serializers.FloatField(required=False)
    payment = serializers.FloatField(required=False)
    sale_type_id = serializers.IntegerField(allow_null=False, required=False)
    total = serializers.FloatField(required=False)
    sale_status = SaleStatusSerializer(required=False)

    class Meta:
        model = Sale
        fields = '__all__'
