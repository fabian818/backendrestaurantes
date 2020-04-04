from json import dumps
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodCategoryFactory
from api.models import FoodCategory

client = Client()
base_list_path = '/api/admin/food_categories/{}/'

food_category_valid_payload = {
    'display_name': 'Pollo ricolino.',
    'description': 'Redbull te da alas.'
}


class PutPatchUpdateFoodCategoryTest(TestCase):
    """ Test module for PATCH/PUT update food_category API """
    def setUp(self):
        self.food_category_valid_payload = food_category_valid_payload
        self.food_category = FoodCategoryFactory()

    def test_update_foods(self):
        food_category_id = self.food_category.id
        response = client.patch(base_list_path.format(self.food_category.id),
                                dumps(self.food_category_valid_payload),
                                content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        food_category = FoodCategory.objects.get(id=food_category_id)
        self.assertEqual(food_category.name, 'pollo-ricolino')
        self.assertEqual(food_category.display_name, 'Pollo ricolino.')
        self.assertEqual(food_category.description, 'Redbull te da alas.')
