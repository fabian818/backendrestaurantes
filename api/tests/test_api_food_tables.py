from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodTableFactory, FoodFactory, FoodOrderFactory
from api.tests.factories.builders import meta_data_specific
from api.meta_data import OrderStatusID


client = Client()
base_list_path = '/api/food_tables/'


class GetListOfFoodTablesTest(TestCase):
    """ Test module for GET list of food_tables API """

    def setUp(self):
        meta_data_specific(['food_category', 'food_status', 'order_status', 'table_status'])
        self.total_created_active = 5
        self.total_created_paid = 3
        self.food_table = FoodTableFactory()
        self.food = FoodFactory()
        for _ in range(self.total_created_active):
            FoodOrderFactory(food_table=self.food_table, food=self.food, sale_id=None)

        for _ in range(self.total_created_paid):
            FoodOrderFactory(food_table=self.food_table, food=self.food, order_status_id=OrderStatusID.PAID, sale_id=None)

    def test_list_of_food_tables(self):
        response = client.get(base_list_path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data[0]['food_orders']), 5)
