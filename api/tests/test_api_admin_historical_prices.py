import random
from rest_framework import status
from django.test import TestCase, Client
from api.models import Food
from api.tests.factories.base import HistoricalPriceFactory, FoodFactory
from api.tests.factories.builders import meta_data_specific

call_client = Client()
base_list_path = '/api/admin/historical_prices'


class GetListHistoricalPricesTest(TestCase):
    """ Test module for GET all historical prices or find by identifier API """
    def setUp(self):
        meta_data_specific(
            ['food_category', 'food_status', 'order_status', 'table_status'])
        self.total_created_foods = 10
        for _ in range(self.total_created_foods):
            FoodFactory()
        self.food = Food.objects.all().first()
        for _ in range(5):
            self.food.price = random.randint(100, 200)
            self.food.save()

    def test_list_of_historical_prices(self):
        response = call_client.get(base_list_path)
        data = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 15)

    def test_filter(self):
        filter_path = base_list_path + '?food_id__in=' + str(self.food.id)
        response = call_client.get(filter_path)

        data = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 6)
        self.assertEqual(data[0]['food'], self.food.id)