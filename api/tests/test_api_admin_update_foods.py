from json import dumps
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodFactory
from api.models import Food
from api.tests.factories.builders import meta_data_specific

client = Client()
base_list_path = '/api/admin/foods/{}/'

food_valid_payload = {
    'food_status': 2,
    'food_category': 2,
    'name': 'Comida de casa',
    'price': 20.00
}


class PutPatchUpdateFoodTest(TestCase):
    """ Test module for PATCH/PUT update food API """
    def setUp(self):
        meta_data_specific(['food_category', 'food_status'])
        self.food_valid_payload = food_valid_payload
        self.food = FoodFactory()

    def test_update_foods(self):
        food_id = self.food.id
        response = client.patch(base_list_path.format(self.food.id),
                                dumps(self.food_valid_payload),
                                content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        food = Food.objects.get(id=food_id)
        self.assertEqual(food.food_status_id, 2)
        self.assertEqual(food.food_category_id, 2)
        self.assertEqual(food.name, 'Comida de casa')
        self.assertEqual(float(food.price), 20.00)
