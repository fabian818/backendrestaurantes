from json import dumps
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodOrderFactory
from api.tests.factories.builders import meta_data_specific
from api.meta_data import OrderStatusID

client = Client()
base_list_path = '/api/food_orders/'


class DeleteFoodOrderTest(TestCase):
    """ Test module for DELETE food order API """
    def setUp(self):
        meta_data_specific([
            'food_category', 'food_status', 'order_status', 'table_status',
            'sale_type', 'sale_status'
        ])
        self.food_order = FoodOrderFactory(price=10.00, sale_id=None)
        self.food_order_with_sale = FoodOrderFactory()
        self.food_order_paid = FoodOrderFactory(order_status_id=3)

    def test_delete_food_order(self):
        complete_path = "{}{}".format(base_list_path, self.food_order.id)
        response = client.delete(complete_path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_status'], OrderStatusID.DELETED)

    def test_delete_food_order_with_sale(self):
        complete_path = "{}{}".format(base_list_path,
                                      self.food_order_with_sale.id)
        response = client.delete(complete_path)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_food_order_paid(self):
        complete_path = "{}{}".format(base_list_path, self.food_order_paid.id)
        response = client.delete(complete_path)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
