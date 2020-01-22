import json
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodTableFactory, FoodFactory, FoodOrderFactory
from api.tests.factories.builders import meta_data_specific
from api.meta_data import OrderStatusID

client = Client()
base_list_path = '/api/food_orders/'


class GetListOfFoodTablesTest(TestCase):
    """ Test module for GET list of food_tables API """
    def setUp(self):
        meta_data_specific(
            ['food_category', 'food_status', 'order_status', 'table_status'])
        self.total_created_active = 51
        self.total_created_paid = 10
        self.total_created_filter_food = 10
        self.food = FoodFactory(name='Ají de Gallina')
        for _ in range(self.total_created_active):
            FoodOrderFactory(sale=None)
        for _ in range(self.total_created_filter_food):
            FoodOrderFactory(food=self.food,
                             sale=None)

    def test_list_of_food_orders(self):
        response = client.get(base_list_path + '?page=1')
        json_content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_content['results']), 50)

    def test_filter_of_food_tables(self):
        filter_path = base_list_path + '?page=1&food__name__icontains=ají de gallina'
        response = client.get(filter_path)
        json_content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_content['results']), 10)
