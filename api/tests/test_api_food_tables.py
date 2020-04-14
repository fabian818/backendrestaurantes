from json import loads
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodTableFactory, FoodFactory, FoodOrderFactory
from api.tests.factories.builders import meta_data_specific
from api.meta_data import OrderStatusID

client = Client()
base_list_path = '/api/food_tables/'
admin_base_list_path = '/api/food_tables/'


class GetListOfFoodTablesTest(TestCase):
    """ Test module for GET list of food_tables API """
    def setUp(self):
        meta_data_specific(
            ['food_category', 'food_status', 'order_status', 'table_status'])
        self.total_created_active = 5
        self.total_created_paid = 3
        self.food_table = FoodTableFactory()
        FoodTableFactory(table_status_id=2)
        FoodTableFactory(table_status_id=3)
        self.food = FoodFactory()
        for _ in range(self.total_created_active):
            FoodOrderFactory(food_table=self.food_table,
                             food=self.food,
                             sale=None)

        for _ in range(self.total_created_paid):
            FoodOrderFactory(food_table=self.food_table,
                             food=self.food,
                             order_status_id=OrderStatusID.PAID,
                             sale=None)

    def test_list_of_food_tables(self):
        response = client.get(base_list_path)
        data = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['results']), 3)
        self.assertEqual(len(data['results'][0]['food_orders']), 5)

    def test_filter_of_food_tables(self):
        filter_path = base_list_path + '?table_status_id__in=1,2'
        response = client.get(filter_path)
        data = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['results']), 2)
        self.assertEqual(data['results'][0]['table_status'], 1)

    def test_admin_list_of_food_tables(self):
        response = client.get(admin_base_list_path)
        data = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['results']), 3)
        self.assertEqual(len(data['results'][0]['food_orders']), 5)

    def test_admin_filter_of_food_tables(self):
        filter_path = admin_base_list_path + '?table_status_id__in=1,2'
        response = client.get(filter_path)
        data = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['results']), 2)
        self.assertEqual(data['results'][0]['table_status'], 1)


class GetListOfMassiveFoodTablesTest(TestCase):
    """ Test module for GET list of food_tables API """
    def setUp(self):
        meta_data_specific(
            ['food_category', 'food_status', 'order_status', 'table_status'])
        self.total_created_active = 1000
        for _ in range(self.total_created_active):
            FoodTableFactory()

    def test_list_of_food_tables(self):
        response = client.get(base_list_path + '?size=1000&page_size=1000')
        data = loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['results']), 1000)
