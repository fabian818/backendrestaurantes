import random
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import ClientFactory

call_client = Client()
base_list_path = '/api/clients/'


class GetListClientsTest(TestCase):
    """ Test module for GET all clients or find by identifier API """
    def setUp(self):
        self.total_created_clients = 10
        for _ in range(self.total_created_clients):
            identifier = str(random.randint(11111111, 99999999))
            ClientFactory(identifier=identifier)

    def test_list_of_clients(self):
        response = call_client.get(base_list_path)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 10)

    def test_filter_of_identifier(self):
        response = call_client.get(base_list_path)
        identifier = response.data[0]['identifier']
        filter_path = base_list_path + '?identifier=' + identifier
        response = call_client.get(filter_path)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['identifier'], identifier)