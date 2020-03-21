from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from petclinic.models import Owner
from petclinic.test_utils import *


class OwnerTests(APITestCase):

    def setUp(self):
        owner = create_owner(email='test_owner_view@example.com')

    def test_retrieve_owners(self):
        """
        Ensure that we can retrieve owners from api service
        """
        url = reverse('owner-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Owner.objects.count(), 1)
        self.assertEqual(len(response.data), 1)
        response.render()
        print(response.content)

class VetTests(APITestCase):

    def setUp(self):
        vet = create_vet(email='test-vet-view@example.com')

    def test_retrieve_vets(self):
        """
        Ensure can retrieve vets from api service
        """
        url=reverse('vet-list')
        response = self.client.get(url, format='json')
        response.render()
        print(response.content)
