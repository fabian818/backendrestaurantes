import json
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import SaleFactory
from api.tests.factories.builders import meta_data_specific
from api.models import Sale


client = Client()
base_list_path = '/api/sales/'


class GetListOfSalesTest(TestCase):
    """ Test module for GET list of sales API """
    def setUp(self):
        meta_data_specific(
            ['food_category', 'food_status', 'order_status', 'table_status', 'sale_status', 'sale_type'])
        self.total_created_active = 51
        for _ in range(self.total_created_active):
            SaleFactory()

    def test_list_of_fo(self):
        response = client.get(base_list_path + '?page=1')
        print(response.content)
        json_content = json.loads(response.content)
        sales = Sale.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_content['results']), 50)
        self.assertEqual(sales.count(), 51)
