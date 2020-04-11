from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import FoodTableFactory, FoodOrderFactory
from api.models import FoodTable
from api.tests.factories.builders import meta_data_specific
from api.meta_data import TableStatusID, OrderStatusID

client = Client()
base_list_path = '/api/admin/food_tables/{}/'


class DeleteFoodTablesTest(TestCase):
    """ Test module for soft DELETE food tables API """
    def setUp(self):
        meta_data_specific(
            ['food_category', 'food_status', 'order_status', 'table_status'])
        self.food_table1 = FoodTableFactory()
        self.food_table2 = FoodTableFactory()
        self.food_table3 = FoodTableFactory()
        self.total_orders_created = 2
        self.total_orders_related = 3
        for _ in range(self.total_orders_created):
            FoodOrderFactory(food_table=self.food_table2,
                             order_status_id=OrderStatusID.CREATED,
                             sale=None)

        for _ in range(self.total_orders_related):
            FoodOrderFactory(food_table=self.food_table3,
                             order_status_id=OrderStatusID.RELATED,
                             sale=None)

    def test_delete_food_tables(self):
        response = client.delete(base_list_path.format(self.food_table1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        food_table = FoodTable.objects.get(id=self.food_table1.id)
        self.assertNotEqual(food_table.deleted_at, None)
        self.assertEqual(food_table.table_status_id, TableStatusID.DELETED)

    def test_delete_food_tables_with_food_orders_created(self):
        response = client.delete(base_list_path.format(self.food_table2.id))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        food_table = FoodTable.objects.get(id=self.food_table2.id)
        self.assertEqual(food_table.deleted_at, None)
        self.assertNotEqual(food_table.table_status_id, TableStatusID.DELETED)

    def test_delete_food_tables_with_food_orders_related(self):
        response = client.delete(base_list_path.format(self.food_table3.id))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        food_table = FoodTable.objects.get(id=self.food_table3.id)
        self.assertEqual(food_table.deleted_at, None)
        self.assertNotEqual(food_table.table_status_id, TableStatusID.DELETED)
