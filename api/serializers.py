from rest_framework import serializers
from api.models import FoodTable, FoodOrder, Food
from api.meta_data import OrderStatusID


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class FoodOrderSerializer(serializers.ModelSerializer):
    food = FoodSerializer()

    class Meta:
        model = FoodOrder
        fields = '__all__'


class FoodTableSerializer(serializers.ModelSerializer):
    food_orders = serializers.SerializerMethodField(source='food_orders', read_only=True)

    class Meta:
        model = FoodTable
        fields = '__all__'

    def get_food_orders(self, obj):
        return FoodOrderSerializer(
            obj.food_orders.filter(order_status_id=OrderStatusID.CREATED),
            many=True,
            read_only=True).data

    class Meta:
        model = FoodTable
        child = FoodOrder
        fields = '__all__'
