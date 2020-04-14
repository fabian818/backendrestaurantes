from json import dumps
from rest_framework import status
from django.test import TestCase, Client
from api.tests.factories.base import ClientFactory

call_client = Client()
base_list_path = '/api/clients/'
client_valid_payload = {
    'identifier': '72446953',
    'name': 'Alvarito',
    'last_name': 'Palacios Carrillo'
}


class PostCreateClientsTest(TestCase):
    """ Test module for POST to create clients API """
    def test_create_clients(self):
        response = call_client.post(base_list_path,
                                    dumps(client_valid_payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data['identifier'], None)
        self.assertNotEqual(response.data['name'], None)
        self.assertNotEqual(response.data['last_name'], None)
