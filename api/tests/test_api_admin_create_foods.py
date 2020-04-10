from json import dumps
from rest_framework import status
from django.test import TestCase, Client
from api.models import HistoricalPrice
from api.tests.factories.builders import meta_data_specific

client = Client()
base_list_path = '/api/admin/foods'
food_valid_payload = {
    'food_status': 1,
    'food_category': 1,
    'name': 'Ají de Gallina',
    'price': 10.00
}


class PostCreateFoodTest(TestCase):
    """ Test module for POST create foods API """
    def setUp(self):
        meta_data_specific(['food_category', 'food_status'])
        self.food_valid_payload = food_valid_payload

    def test_create_foods(self):
        response = client.post(base_list_path,
                               dumps(self.food_valid_payload),
                               content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['price']), 10.00)
        self.assertEqual(response.data['food_status'], 1)
        self.assertEqual(response.data['food_category'], 1)
        historical_prices = HistoricalPrice.objects.all()
        self.assertEqual(historical_prices.count(), 1)
        self.assertEqual(historical_prices.first().price, 10.00)
