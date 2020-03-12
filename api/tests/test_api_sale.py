from json import dumps
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodTableFactory, FoodFactory, FoodOrderFactory, ClientFactory
from api.models import FoodOrder
from api.tests.factories.builders import meta_data_specific
from api.meta_data import OrderStatusID

client = Client()
base_list_path = '/api/sales/'
sale_valid_payload = {
    'food_orders': None,
    'client_id': None,
    'payment': 550.00,
    'sale_type_id': 2,
    'sale_status_id': 2
}


class PostCreateSaleTest(TestCase):
    """ Test module for POST create sale API """
    def setUp(self):
        meta_data_specific([
            'food_category', 'food_status', 'order_status', 'table_status',
            'sale_status', 'sale_type'
        ])
        self.sale_valid_payload = sale_valid_payload
        self.food_table = FoodTableFactory()
        self.food = FoodFactory()
        self.total_created_paid = 3
        self.food_orders = []
        for _ in range(self.total_created_paid):
            food_order_factory = FoodOrderFactory(
                quantity=1,
                price=10.00,
                food_table=self.food_table,
                food=self.food,
                order_status_id=OrderStatusID.CREATED,
                sale_id=None)
            self.food_orders.append(food_order_factory.id)

        self.sale_valid_payload = sale_valid_payload
        self.sale_valid_payload['food_orders'] = self.food_orders
        self.client = ClientFactory()
        self.sale_valid_payload['client_id'] = self.client.id

    def test_create_sales(self):
        response = client.post(base_list_path,
                               dumps(self.sale_valid_payload),
                               content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total'], 30.0)
        self.assertNotEqual(response.data['code'], None)
        self.assertNotEqual(response.data['code'], 'B001-00000001')
        self.assertNotEqual(response.data['payment'], None)
        self.assertEqual(response.data['change'],
                         response.data['payment'] - response.data['total'])
        self.assertEqual(response.data['sale_type_id'], 2)
        self.assertEqual(response.data['sale_status_id'], 2)
        self.assertEqual(len(FoodOrder.objects.filter(sale_id=response.data['id'])), self.total_created_paid)
        for food_order in FoodOrder.objects.filter(sale_id=response.data['id']):
            self.assertEqual(food_order.order_status_id, OrderStatusID.PAID)
