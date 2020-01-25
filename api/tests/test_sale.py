from json import dumps
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodTableFactory, FoodFactory, FoodOrderFactory
from api.tests.factories.builders import meta_data_specific
from api.meta_data import OrderStatusID

client = Client()
base_list_path = '/api/food_orders/bulk_create/'
sale_valid_payload = {
    'food_orders': None,
    'client': {
        'identifier': '72446953',
        'name': 'Alvaro',
        'last_name': 'Palacios'
    },
    'payment': 50.00
}


class PostBulkCreateSalesTest(TestCase):
    """ Test module for GET list of food_tables API """
    def setUp(self):
        meta_data_specific(
            ['food_category', 'food_status', 'order_status', 'table_status'])
        self.sale_valid_payload = sale_valid_payload
        self.food_table = FoodTableFactory()
        self.food = FoodFactory(price=10.00)
        self.total_created_paid = 3
        self.food_orders = []
        for _ in range(self.total_created_paid):
            self.food_orders.append(
                FoodOrderFactory(food_table=self.food_table,
                                 food=self.food,
                                 order_status_id=OrderStatusID.PAID))

        self.sale_valid_payload = sale_valid_payload
        self.sale_valid_payload['food_orders'] = self.food_orders

    def test_create_sales(self):
        response = client.post(base_list_path,
                               dumps(self.sale_valid_payload),
                               content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total'], self.food['price'] * 3)
        self.assertNotEqual(response.data['code'], None)
        self.assertNotEqual(response.data['payment'], None)
        self.assertEqual(response.data['change'],
                         response.data['payment'] - response.data['total'])
        # Acá deben ir los tests de client
