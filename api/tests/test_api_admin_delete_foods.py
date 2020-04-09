from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodFactory
from api.models import Food
from api.tests.factories.builders import meta_data_specific
from api.meta_data import FoodStatusID

client = Client()
base_list_path = '/api/admin/foods/{}/'


class DeleteFoodTest(TestCase):
    """ Test module for soft DELETE foods API """
    def setUp(self):
        meta_data_specific(['food_category', 'food_status'])
        self.food = FoodFactory()

    def test_delete_foods(self):
        response = client.delete(base_list_path.format(self.food.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        food = Food.objects.get(id=self.food.id)
        self.assertNotEqual(food.deleted_at, None)
        self.assertEqual(food.food_status_id, FoodStatusID.DELETED)
