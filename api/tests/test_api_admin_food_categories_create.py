from json import dumps
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.builders import meta_data_specific

client = Client()
base_list_path = '/api/admin/food_categories'
food_category_valid_payload = {
    'name': 'Tamales',
    'display_name': 'Desayuno',
    'description': 'Descripción del desayuno'
}


class PostCreateFoodCategoryTest(TestCase):
    """ Test module for POST create food category API """
    def setUp(self):
        self.food_category_valid_payload = food_category_valid_payload

    def test_create_food_categories(self):
        response = client.post(base_list_path,
                               dumps(self.food_category_valid_payload),
                               content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Tamales')
        self.assertEqual(response.data['display_name'], 'Desayuno')
        self.assertEqual(response.data['description'],
                         'Descripción del desayuno')
