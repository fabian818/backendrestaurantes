import random
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodCategoryFactory

call_client = Client()
base_list_path = '/api/admin/food_categories'


class GetListFoodCategoriesTest(TestCase):
    """ Test module for GET all food categories or find by identifier API """
    def setUp(self):
        self.total_created_food_categories = 10
        for _ in range(self.total_created_food_categories):
            FoodCategoryFactory()

    def test_list_of_food_categories(self):
        response = call_client.get(base_list_path)
        data = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 10)

    def test_filter(self):
        response = call_client.get(base_list_path)
        data = response.data['results']
        name = data[0]['name']
        display_name = data[0]['display_name']

        filter_path = base_list_path + '?name=' + name
        response = call_client.get(filter_path)

        data = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], name)

        filter_path = base_list_path + '?display_name=' + display_name
        response = call_client.get(filter_path)

        data = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['display_name'], display_name)