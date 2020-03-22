from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from petclinic.models import Owner
from petclinic.test_utils import *


class OwnerListTests(APITestCase):

    def setUp(self):
        self.owner = create_owner(email='test_owner_view@example.com')
        self.url = reverse('owner-list')

    def test_retrieve_owners(self):
        """
        Ensure that we can retrieve owners from api service
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Owner.objects.count(), 1)
        self.assertEqual(len(response.data), 1)

    def test_create_owner(self):
        """
        Ensure that an owner can be created
        """
        owner_data = { 'email': 'test-new-owner@example.com', 'last_name': 'Last', 
                        'first_name': 'First', 'street_address': '1234 Main St', 
                        'city': 'Dublin', 'state': 'CA', 'telephone': '1-408-555-1212', 
                        }
        response = self.client.post(self.url, owner_data, format='json')
        own_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(own_obj['email'], 'test-new-owner@example.com')

class OwnerDetailTests(APITestCase):

    def setUp(self):
        self.owner = create_owner(email='test_owner_view@example.com')
        self.url = reverse('owner-detail', args=[self.owner.id])

    def test_retrieve_owner_by_pk(self):
        """
        Ensure that owner can be retrieved by primary key id
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        ret_obj = json.loads(response.content)
        self.assertEqual(ret_obj['email'], self.owner.email)
 
    def test_update_owner_by_pk(self):
        """
        Ensure an owner can be updated
        """
        o_data = { 'first_name': 'change_fname', 'last_name': 'changed_lname'}
        response = self.client.put(self.url, o_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(ret_obj['last_name'], o_data['last_name'])
        self.assertEqual(ret_obj['first_name'], o_data['first_name'])

    def test_delete_owner_by_pk(self):
        """
        Ensure that an owner can be removed from the database
        """
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Owner.objects.count(), 0)

class VetListTests(APITestCase):

    def setUp(self):
        self.vet = create_vet(email='test-vet-view@example.com')
        self.url=reverse('vet-list')

    def test_retrieve_vets(self):
        """
        Ensure can retrieve vets from api service
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vet(self):
        """
        Ensure a new vet can be created
        """
        specialty = create_specialty('jogging')
        vet_data = {'email': 'test-new-owner@example.com', 'last_name': 'Last', 
                        'first_name': 'First', 'street_address': '1234 Main St', 
                        'city': 'Dublin', 'state': 'CA', 'telephone': '1-408-555-1212',
                        'specialty': specialty.id}
        response = self.client.post(self.url, vet_data, format='json')
        vet_obj = json.loads(response.content)
        sp = Specialty.objects.get(pk=vet_obj['specialty'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(sp.name, specialty.name)
        self.assertEqual(vet_obj['email'], 'test-new-owner@example.com')

class VetDetailTests(APITestCase):

    def setUp(self):
        self.specialty = create_specialty('dancing')
        self.vet = create_vet(email='test-vet-detail@example.com')
        self.vet.specialty = self.specialty
        self.vet.save()
        self.url = reverse('vet-detail', args=[self.vet.id])

    def test_retrieve_vet_by_pk(self):
        """
        Ensure a vet can be looked up by id
        """
        response = self.client.get(self.url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ret_obj['id'], self.vet.id)


    def test_update_vet_by_pk(self):
        """
        Ensure a vet can be updated in DB
        """
        v_data = { 'city': 'Mountain View', 'state': 'CA'}
        response = self.client.put(self.url, v_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ret_obj['id'], self.vet.id)
        self.assertEqual(ret_obj['city'], v_data['city'])
        self.assertEqual(ret_obj['state'], v_data['state'])

    def test_delete_vet_by_pk(self):
        """
        Ensure a vet can be removed from DB
        """
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vet.objects.count(), 0)
