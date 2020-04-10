from json import dumps
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodTableFactory
from api.models import FoodTable
from api.tests.factories.builders import meta_data_specific

client = Client()
base_list_path = '/api/admin/food_tables/{}/'

food_table_valid_payload = {
    'table_status': 2,
    'display_name': 'Mesa 2',
    'description': 'Nueva Descripción de la mesa'
}


class PutPatchUpdateFoodTableTest(TestCase):
    """ Test module for PATCH/PUT update tables API """
    def setUp(self):
        meta_data_specific(['table_status'])
        self.food_table_valid_payload = food_table_valid_payload
        self.food_table = FoodTableFactory()

    def test_update_food_tables(self):
        food_table_id = self.food_table.id
        response = client.patch(base_list_path.format(food_table_id),
                                dumps(self.food_table_valid_payload),
                                content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        food_table = FoodTable.objects.get(id=food_table_id)
        self.assertEqual(food_table.table_status_id, 2)
        self.assertEqual(food_table.identifier, 'mesa-2')
        self.assertEqual(food_table.display_name, 'Mesa 2')
        self.assertEqual(food_table.description, 'Nueva Descripción de la mesa')
