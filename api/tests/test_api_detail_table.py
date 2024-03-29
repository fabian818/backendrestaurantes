from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodTableFactory, FoodFactory, FoodOrderFactory
from api.tests.factories.builders import meta_data_specific
from api.meta_data import OrderStatusID

client = Client()
base_list_path = '/api/food_tables/{}'


class GetDetailFoodTableTest(TestCase):
    """ Test module for GET a single food_table API """
    def setUp(self):
        meta_data_specific(['food_category', 'food_status', 'order_status', 'table_status'])
        self.total_created_canceled = 10
        self.food_table = FoodTableFactory()
        self.food = FoodFactory()
        FoodOrderFactory(food_table=self.food_table,
                            food=self.food,
                            sale=None)

        FoodOrderFactory(food_table=self.food_table,
                            food=self.food,
                            order_status_id=OrderStatusID.PAID,
                            sale=None)

        for _ in range(self.total_created_canceled):
            FoodOrderFactory(food_table=self.food_table,
                             food=self.food,
                             order_status_id=OrderStatusID.CANCELED,
                             sale=None)

    def test_food_table(self):
        response = client.get(base_list_path.format(self.food_table.id))
        data = response.data
        self.assertEqual(data['table_status'], 1)
        self.assertNotEqual(data['identifier'], None)
        self.assertNotEqual(data['display_name'], None)
        self.assertNotEqual(data['description'], None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 9)
        self.assertEqual(len(data['food_orders']), 1)
