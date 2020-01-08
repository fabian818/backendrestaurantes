from rest_framework import status
from django.test import TestCase, Client
from api.models import FoodTable
from api.tests.factories.base import AccountFactory, UserFactory
from api.tests.factories.builders import meta_data_specific

client = Client()

base_list_path = '/api/food_tables/'

class GetListOfAccountsTest(TestCase):
    """ Test module for GET list of food_tables API """

    def setUp(self):
        meta_data_specific(['code_types', 'account_types', 'account_status'])
        self.total_created = 5
        for _ in range(self.total_created):
            AccountFactory()

    def test_list_of_account(self):
        response = client.get(base_list_path.format(User.objects.last().id))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)