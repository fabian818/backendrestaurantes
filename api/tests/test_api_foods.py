import json
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodFactory
from api.tests.factories.builders import meta_data_specific
from api.models import Sale, Client as ClientModel


client = Client()
base_list_path = '/api/foods/'


class GetListOfSalesTest(TestCase):
    """ Test module for GET list of sales API """
    def setUp(self):
        meta_data_specific(
            ['food_category', 'food_status'])
        self.total_created_active = 51
        for _ in range(self.total_created_active):
            FoodFactory()

    def test_list_of_sales(self):
        response = client.get(base_list_path)
        json_content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_content), 51)
