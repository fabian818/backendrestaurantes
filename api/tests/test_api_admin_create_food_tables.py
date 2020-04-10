from json import dumps
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.builders import meta_data_specific

client = Client()
base_list_path = '/api/admin/food_tables'
food_table_valid_payload = {
    'display_name': 'Mesa 1',
    'description': 'Descripción de la mesa'
}


class PostCreateFoodTableTest(TestCase):
    """ Test module for POST create food table API """
    def setUp(self):
        meta_data_specific(['table_status'])
        self.food_table_valid_payload = food_table_valid_payload

    def test_create_food_categories(self):
        response = client.post(base_list_path,
                               dumps(self.food_table_valid_payload),
                               content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['table_status'], 1)
        self.assertEqual(response.data['identifier'], 'mesa-1')
        self.assertEqual(response.data['display_name'], 'Mesa 1')
        self.assertEqual(response.data['description'],
                         'Descripción de la mesa')
