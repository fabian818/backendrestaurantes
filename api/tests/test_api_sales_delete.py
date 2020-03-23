from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodTableFactory, FoodOrderFactory, SaleFactory
from api.models import FoodOrder, Sale
from api.tests.factories.builders import meta_data_specific
from api.meta_data import OrderStatusID, SaleStatusID

client = Client()
base_list_path = '/api/sales/{}/'


class DeleteSaleTest(TestCase):
    """ Test module for DELETE update sale API """

    def setUp(self):
        meta_data_specific([
            'food_category', 'food_status', 'order_status', 'table_status',
            'sale_status', 'sale_type'
        ])
        self.sale = SaleFactory(sale_status_id=SaleStatusID.CREATED)
        self.table = FoodTableFactory()
        for _ in range(5):
            FoodOrderFactory(sale=self.sale, food_table=self.table, order_status_id=OrderStatusID.RELATED)

    def test_update_sales(self):
        response = client.delete(base_list_path.format(self.sale.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        sale = Sale.objects.get(id=self.sale.id)
        food_orders = FoodOrder.objects.filter(sale_id=self.sale.id)
        self.assertEqual(sale.sale_status_id, SaleStatusID.DELETED)
        for order in food_orders:
            self.assertEqual(order.order_status_id, OrderStatusID.CREATED)
