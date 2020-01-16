from json import dumps
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodTableFactory, FoodFactory
from api.tests.factories.builders import meta_data_specific
from api.meta_data import OrderStatusID

client = Client()
base_list_path = '/api/food_orders/bulk_create/'
food_order_valid_payload = {
    'food_table_id': None,
    'food_orders': [
        {
            "price": 15.99,
            "quantity": 2,
            "food_id": None
        }
    ]
}


class PostBulkCreateFoodOrdersTest(TestCase):
    """ Test module for GET list of food_tables API """

    def setUp(self):
        meta_data_specific(['food_category', 'food_status', 'order_status', 'table_status'])
        self.food_table = FoodTableFactory()
        self.food = FoodFactory(price=15.99)
        self.food_order_valid_payload = food_order_valid_payload
        self.food_order_valid_payload['food_table_id'] = self.food_table.id
        self.food_order_valid_payload['food_orders'][0]['food_id'] = self.food.id

    def test_create_food_orders(self):
        response = client.post(
            base_list_path,
            dumps(self.food_order_valid_payload),
            content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['food_table_id'], self.food_table.id)
        self.assertEqual(
            response.data['food_orders'][0]['total'],
            self.food_order_valid_payload['food_orders']
            [0]['price'] * self.food_order_valid_payload['food_orders']
            [0]['quantity'])
        self.assertEqual(
            response.data['food_orders'][0]['order_status_id'], OrderStatusID.CREATED)
        self.assertEqual(
            response.data['food_orders'][0]['food_table_id'], self.food_table.id)
        self.assertEqual(len(response.data['food_orders']), 1)
