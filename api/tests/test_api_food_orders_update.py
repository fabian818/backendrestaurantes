from json import dumps
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodOrderFactory, FoodFactory
from api.tests.factories.builders import meta_data_specific

client = Client()
base_list_path = '/api/food_orders/'
food_order_update = {
    "quantity": 10,
    "food_id": None,
    "food_table_id": None
}


class UpdateFoodOrderTest(TestCase):
    """ Test module for UPDATE food order API """
    def setUp(self):
        meta_data_specific([
            'food_category', 'food_status', 'order_status', 'table_status',
            'sale_type', 'sale_status'
        ])
        self.food = FoodFactory()
        self.food_order = FoodOrderFactory(price=10.00, sale_id=None)
        self.food_order_with_sale = FoodOrderFactory()
        self.food_order_paid = FoodOrderFactory(order_status_id=3)
        self.food_order_update = food_order_update
        self.food_order_update['food_id'] = self.food.id
        self.food_order_update['food_table_id'] = self.food_order.food_table_id

    def test_update_food_order(self):
        complete_path = "{}{}".format(base_list_path, self.food_order.id)
        response = client.put(complete_path,
                              dumps(self.food_order_update),
                              content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        total = self.food.price * self.food_order_update['quantity']
        price = self.food.price
        self.assertEqual(response.data['price'], price)
        self.assertEqual(response.data['total'], total)
        self.assertEqual(response.data['quantity'], 10)
        self.assertEqual(response.data['sale'], None)

    def test_update_food_order_with_sale(self):
        complete_path = "{}{}".format(base_list_path, self.food_order_with_sale.id)
        response = client.put(complete_path,
                              dumps(self.food_order_update),
                              content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_food_order_paid(self):
        complete_path = "{}{}".format(base_list_path, self.food_order_paid.id)
        response = client.put(complete_path,
                              dumps(self.food_order_update),
                              content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
