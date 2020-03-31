import random
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodFactory
from api.tests.factories.builders import meta_data_specific

call_client = Client()
base_list_path = '/api/admin/foods'


class GetListFoodCategoriesTest(TestCase):
    """ Test module for GET all foods or find by identifier API """
    def setUp(self):
        meta_data_specific(
            ['food_category', 'food_status', 'order_status', 'table_status'])
        self.total_created_foods = 10
        for _ in range(self.total_created_foods):
            FoodFactory()

        self.total_created_foods_lunch = 2
        for _ in range(self.total_created_foods_lunch):
            FoodFactory(food_category_id=2)

        self.total_created_foods_inactives = 3
        for _ in range(self.total_created_foods_inactives):
            FoodFactory(food_status_id=2)

    def test_list_of_foods(self):
        response = call_client.get(base_list_path)
        data = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 15)

    def test_filter(self):
        filter_path = base_list_path + '?food_category_id__in=2'
        response = call_client.get(filter_path)

        data = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['food_category'], 2)

        filter_path = base_list_path + '?food_status_id__in=2'
        response = call_client.get(filter_path)

        data = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['food_status'], 2)