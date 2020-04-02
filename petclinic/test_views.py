from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.state import User

from petclinic.test_utils import *

class BasePetClinicTest(APITestCase):

    def get_credentials(self):
        username = 'test_user'
        password = 'test_passwd_123'
        user = User.objects.create_user(
            username = username,
            password = password
        )
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, data = {
            User.USERNAME_FIELD: username,
            'password': password,
        },)
        access_token = response.data['access']
        return '{} {}'.format('Bearer', access_token)

class OwnerListTests(BasePetClinicTest):

    def setUp(self):
        self.owner = create_owner(email='test_owner_view@example.com')
        self.url = reverse('owner-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.get_credentials())
        

    def test_retrieve_owners(self):
        """
        Ensure that we can retrieve owners from api service
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Owner.objects.count(), 1)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_owners_filtered_by_state(self):
        owner1 = create_owner(email='test_owner_ca@example.com', state='CA')
        owner2 = create_owner(email='test_owner_tx@example.com', state='TX')
        state_url = "%s?state=TX" % self.url
        response = self.client.get(state_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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

    def test_create_owner_fails_if_email_already_exists(self):
        """
        Ensure that an owner cannot be created if email already exists
        """
        owner = create_owner(email='test-new-owner@example.com')
        owner_data = { 'email': 'test-new-owner@example.com', 'last_name': 'Last', 
                        'first_name': 'First', 'street_address': '1234 Main St', 
                        'city': 'Dublin', 'state': 'CA', 'telephone': '1-408-555-1212', 
                        }
        response = self.client.post(self.url, owner_data, format='json')
        own_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(own_obj['email'][0], 'owner with this email already exists.')

    def test_owner_create_fails_for_required_email_field(self):
        """
        Ensure that an owner will not be created if a required field is missing
        """
        owner_data = { 'last_name': 'Last', 
                        'first_name': 'First', 'street_address': '1234 Main St', 
                        'city': 'Dublin', 'state': 'CA', 'telephone': '1-408-555-1212', 
                        }
        response = self.client.post(self.url, owner_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertTrue(ret_obj['email'][0] == 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_owner_create_fails_if_last_name_is_missing(self):
        """
        Ensure that an owner cannot be created if last name is missing
        """
        owner_data = { 'email': 'test-new-owner@example.com',  
                        'first_name': 'First', 'street_address': '1234 Main St', 
                        'city': 'Dublin', 'state': 'CA', 'telephone': '1-408-555-1212', 
                        }
        response = self.client.post(self.url, owner_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret_obj['last_name'][0], 'This field is required.')

    def test_create_owner_fails_for_invalid_email_address(self):
        """
        Ensure that an owner can be created
        """
        owner_data = { 'email': 'test-new-owner', 'last_name': 'Last', 
                        'first_name': 'First', 'street_address': '1234 Main St', 
                        'city': 'Dublin', 'state': 'CA', 'telephone': '1-408-555-1212', 
                        }
        response = self.client.post(self.url, owner_data, format='json')
        own_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(own_obj['email'][0], 'Enter a valid email address.')

class OwnerDetailTests(BasePetClinicTest):

    def setUp(self):
        self.owner = create_owner(email='test_owner_view@example.com')
        self.url = reverse('owner-detail', args=[self.owner.id])
        self.bad_url = reverse('owner-detail', args=[10000])
        self.client.credentials(HTTP_AUTHORIZATION=self.get_credentials())

    def test_retrieve_owner_by_pk(self):
        """
        Ensure that owner can be retrieved by primary key id
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        ret_obj = json.loads(response.content)
        self.assertEqual(ret_obj['email'], self.owner.email)

    def test_retrieve_owner_by_pk_fails(self):
        """
        Ensure that NOT FOUND status returned for bad id
        """
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 

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

    def test_update_owner_by_pk_fails_invalid_email(self):
        """
        Ensure an owner update fails if email invalid
        """
        o_data = { 'email': 'change_fname', 'last_name': 'changed_lname'}
        response = self.client.put(self.url, o_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)        
        self.assertEqual(ret_obj['email'][0], 'Enter a valid email address.')

    def test_update_owner_by_pk_fails_for_bad_ID(self):
        """
        Ensure an owner can be updated
        """
        o_data = { 'first_name': 'change_fname', 'last_name': 'changed_lname'}
        response = self.client.put(self.bad_url, o_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(ret_obj['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        

    def test_delete_owner_by_pk(self):
        """
        Ensure that an owner can be removed from the database
        """
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Owner.objects.count(), 0)

    def test_delete_owner_by_pk_fails_for_bad_ID(self):
        """
        Ensure that an owner delete fails for bad ID
        """
        response = self.client.delete(self.bad_url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(ret_obj['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Owner.objects.count(), 1)

class VetListTests(BasePetClinicTest):

    def setUp(self):
        self.specialty = create_specialty('testing-filters')
        self.vet = create_vet(email='test-vet-view@example.com', specialty=self.specialty)
        self.url=reverse('vet-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.get_credentials())

    def test_retrieve_vets(self):
        """
        Ensure can retrieve vets from api service
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_vets_filtered_by_state(self):
        vet1 = create_vet(email='test_vet_ca@example.com', state='CA', specialty=self.specialty)
        vet2 = create_vet(email='test_vet_tx@example.com', state='TX', specialty=self.specialty)
        state_url = "%s?state=TX" % self.url
        response = self.client.get(state_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

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

    def test_create_vet_fails_email_already_exists(self):
        """
        Ensure a new vet cannot be created if email already exists
        """
        owner = create_vet(email='test-new-owner@example.com')
        specialty = create_specialty('jogging')
        vet_data = {'email': 'test-new-owner@example.com', 'last_name': 'Last', 
                        'first_name': 'First', 'street_address': '1234 Main St', 
                        'city': 'Dublin', 'state': 'CA', 'telephone': '1-408-555-1212',
                        'specialty': specialty.id}
        response = self.client.post(self.url, vet_data, format='json')
        vet_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(vet_obj['email'][0], 'vet with this email already exists.')

    def test_create_vet_fails_for_missing_email(self):
        """
        Ensure a new vet cannot be created without an email
        """
        specialty = create_specialty('jogging')
        vet_data = {'last_name': 'Last', 
                        'first_name': 'First', 'street_address': '1234 Main St', 
                        'city': 'Dublin', 'state': 'CA', 'telephone': '1-408-555-1212',
                        'specialty': specialty.id}
        response = self.client.post(self.url, vet_data, format='json')
        vet_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(vet_obj['email'][0], 'This field is required.')

    def test_create_vet_fails_for_invalid_email(self):
        """
        Ensure a new vet cannot be created without an email
        """
        specialty = create_specialty('jogging')
        vet_data = {'last_name': 'Last', 'email': 'hello world',
                        'first_name': 'First', 'street_address': '1234 Main St', 
                        'city': 'Dublin', 'state': 'CA', 'telephone': '1-408-555-1212',
                        'specialty': specialty.id}
        response = self.client.post(self.url, vet_data, format='json')
        vet_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(vet_obj['email'][0], 'Enter a valid email address.')

    def test_create_vet_fails_for_missing_field(self):
        """
        Ensure a new vet cannot be created without last name
        """
        specialty = create_specialty('jogging')
        vet_data = {'email': 'test-new-owner@example.com',
                        'first_name': 'First', 'street_address': '1234 Main St', 
                        'city': 'Dublin', 'state': 'CA', 'telephone': '1-408-555-1212',
                        'specialty': specialty.id}
        response = self.client.post(self.url, vet_data, format='json')
        vet_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(vet_obj['last_name'][0], 'This field is required.')

class VetDetailTests(BasePetClinicTest):

    def setUp(self):
        self.specialty = create_specialty('dancing')
        self.vet = create_vet(email='test-vet-detail@example.com')
        self.vet.specialty = self.specialty
        self.vet.save()
        self.url = reverse('vet-detail', args=[self.vet.id])
        self.bad_url = reverse('vet-detail', args=[10000])
        self.client.credentials(HTTP_AUTHORIZATION=self.get_credentials())

    def test_retrieve_vet_by_pk(self):
        """
        Ensure a vet can be looked up by id
        """
        response = self.client.get(self.url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ret_obj['id'], self.vet.id)

    def test_retrieve_vet_by_pk_fails_with_bad_ID(self):
        """
        Ensure a vet retrieval fails as expected with bad ID
        """
        response = self.client.get(self.bad_url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ret_obj['detail'], 'Not found.')

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

    def test_update_vet_by_pk_fails_with_invalid_email(self):
        """
        Ensure a vet update fails if email invalid
        """
        v_data = { 'email': 'Mountain View', 'state': 'CA'}
        response = self.client.put(self.url, v_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret_obj['email'][0], 'Enter a valid email address.')

    def test_update_vet_by_pk_falis_with_bad_ID(self):
        """
        Ensure a vet update fails as expected with bad ID
        """
        v_data = { 'city': 'Mountain View', 'state': 'CA'}
        response = self.client.put(self.bad_url, v_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ret_obj['detail'], 'Not found.')

    def test_delete_vet_by_pk(self):
        """
        Ensure a vet can be removed from DB
        """
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vet.objects.count(), 0)

    def test_delete_vet_by_pk_fails_with_bad_ID(self):
        """
        Ensure a vet delete fails as expected wit bad ID
        """
        response = self.client.delete(self.bad_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        ret_obj = json.loads(response.content)
        self.assertEqual(Vet.objects.count(), 1)
        self.assertEqual(ret_obj['detail'], 'Not found.')

class SpecialtyListTests(BasePetClinicTest):
    """
    Retrieve or create Specialties
    """

    def setUp(self):
        self.specialty = create_specialty('unit-testing')
        self.url = reverse('specialty-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.get_credentials())

    def test_retrieve_all_specialties(self):
        response = self.client.get(self.url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ret_obj[0]['name'], self.specialty.name)

    def test_create_specialty(self):
        """
        Ensure a specialty can be created
        """
        spec_data = { 'name': 'spec-testing'}
        response = self.client.post(self.url, spec_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ret_obj['name'], spec_data['name'])

    def test_create_specialty_fails_invalid_fields(self):
        """
        Ensure specialty createion fails if name field is missing
        """
        spec_data = { 'invalid': 'spec-testing'}
        response = self.client.post(self.url, spec_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret_obj['name'][0], 'This field is required.')

    def test_create_specialty_fails_already_exists(self):
        """
        Ensure specialty creation fails if specialty already exists
        """
        specialty = create_specialty('spec-testing')
        spec_data = { 'name': 'spec-testing'}
        response = self.client.post(self.url, spec_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret_obj['name'][0], 'specialty with this name already exists.')

class SpecialtyDetailTests(BasePetClinicTest):

    def setUp(self):
        self.specialty = create_specialty('unit-testing')
        self.url = reverse('specialty-detail', args=[self.specialty.id])
        self.client.credentials(HTTP_AUTHORIZATION=self.get_credentials())

    def test_retrieve_by_pk(self):
        """
        Ensure specialty can be retrieved by PK
        """
        response = self.client.get(self.url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_by_pk(self):
        """
        Ensure specialty object can be updated
        """
        spec_data = { 'name': 'updated-specialty'}
        response = self.client.put(self.url, spec_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ret_obj['name'], spec_data['name'])

    def test_delete_by_pk(self):
        """
        Ensure that a specialty cannot be deleted
        """
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class PetTypeListTests(BasePetClinicTest):

    def setUp(self):
        self.pet_type = create_pet_type('test-pet-type')
        self.url = reverse('pet-type-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.get_credentials())

    def test_retrieve_all_pet_types(self):
        """
        Ensure all pet types can be retieved
        """
        response = self.client.get(self.url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_pet_type(self):
        """
        Ensure pet type can be created
        """
        pet_type_data = { 'name': 'pet-type-testing'}
        response = self.client.post(self.url, pet_type_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  

    def test_create_pet_type_fails_if_already_exists(self):
        """
        Ensure pet type creation fails if already exists
        """
        pet_type = create_pet_type('pet-type-testing')
        pet_type_data = { 'name': 'pet-type-testing'}
        response = self.client.post(self.url, pet_type_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(ret_obj['name'][0], 'pet type with this name already exists.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  

    def test_create_pet_type_fails_if_invalid_fields(self):
        """
        Ensure pet type creation fails if name field missing
        """
        pet_type_data = { 'bad_field': 'pet-type-testing'}
        response = self.client.post(self.url, pet_type_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(ret_obj['name'][0], 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  

class PetTypeDetailTests(BasePetClinicTest):

    def setUp(self):
        self.pet_type = create_pet_type(pet_type_name='eagle')
        self.url = reverse('pet-type-detail', args=[self.pet_type.id])
        self.bad_url = reverse('pet-type-detail', args=[10000])
        self.client.credentials(HTTP_AUTHORIZATION=self.get_credentials())

    def test_retrieve_by_pk(self):
        """
        Ensure pet type can be retireveed by PK
        """
        response = self.client.get(self.url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ret_obj['id'], self.pet_type.id)

    def test_retrieve_by_pk_fails_bad_ID(self):
        """
        Ensure pet type retrieveal fails as expected for bad ID
        """
        response = self.client.get(self.bad_url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ret_obj['detail'], 'Not found.')

    def test_update_by_pk(self):
        """
        Ensure pet type can be updated 
        """
        pet_type_data = { 'name': 'updated-pet-type'}
        response = self.client.put(self.url, pet_type_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ret_obj['name'], pet_type_data['name'])

    def test_update_by_pk_fails_already_exists(self):
        """
        Ensure pet type update fails if pet type with name already exists
        """
        pet_type = create_pet_type('updated-pet-type')
        pet_type_data = { 'name': 'updated-pet-type'}
        response = self.client.put(self.url, pet_type_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret_obj['name'][0], 'pet type with this name already exists.')

    def test_update_by_pk_fails_bad_ID(self):
        """
        Ensure pet type can be updated 
        """
        pet_type_data = { 'name': 'updated-pet-type'}
        response = self.client.put(self.bad_url, pet_type_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ret_obj['detail'], 'Not found.')

    def test_delete_by_pk(self):
        """
        Ensure that a pet type cannot be deleted from API
        """
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class OwnerPetListTests(BasePetClinicTest):

    def setUp(self):
        self.owner = create_owner(email='test-owner-pet-list@example.com')
        self.pet_type = create_pet_type('test-pet-type')
        self.pets = [ 
            create_pet(owner=self.owner, name='pet1'),
            create_pet(owner=self.owner, name='pet2')
        ]
        self.url = reverse('owner-pet-list', args=[self.owner.id])
        self.client.credentials(HTTP_AUTHORIZATION=self.get_credentials())

    def test_retrieve_all_pets_for_owner(self):
        """
        Ensure pets can be retrieved for a given owner
        """
        response = self.client.get(self.url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(ret_obj), 2)
        self.assertEqual(ret_obj[0]['owner'], self.owner.id)
        self.assertEqual(ret_obj[1]['owner'], self.owner.id)

    def test_create_new_pets_for_owner(self):
        """
        Ensure pets can be added to an owner
        """
        pets_data = [
            { 'name': 'pet1', 'pet_type': self.pet_type.id, 'birth_date': timezone.now().date() },
            { 'name': 'pet2', 'pet_type': self.pet_type.id, 'birth_date': timezone.now().date() }
        ]
        response = self.client.post(self.url, pets_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(ret_obj), 2)
        self.assertEqual(ret_obj[0]['pet_type'], self.pet_type.id)
        self.assertEqual(ret_obj[0]['name'], 'pet1')
        self.assertEqual(ret_obj[1]['name'], 'pet2')
        self.assertEqual(ret_obj[0]['owner'], self.owner.id)
        self.assertEqual(ret_obj[1]['owner'], self.owner.id)

class PetVisitListTests(BasePetClinicTest):
    
    def setUp(self):
        self.owner = create_owner()
        self.pet_type = create_pet_type('test-pet-type')
        self.pet = create_pet(owner=self.owner)
        self.visits = [
            create_visit(pet=self.pet),
            create_visit(pet=self.pet)
        ]
        self.url = reverse('pet-visit-list', args=[self.pet.id])
        self.client.credentials(HTTP_AUTHORIZATION=self.get_credentials())
    
    def test_retrieve_all_visits_for_pet(self):
        """
        Ensure vists can be retrieved for a pet
        """
        response = self.client.get(self.url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(ret_obj), 2)
        self.assertEqual(ret_obj[0]['pet'], self.pet.id)
        self.assertEqual(ret_obj[1]['pet'], self.pet.id)

    def test_create_new_visits_for_pet(self):
        """
        Ensure that you can add a list of vists to a pet
        """
        visits_data = [
            { 'visit_date': timezone.now(), 'description': 'test' },
            { 'visit_date': timezone.now(), 'description': 'test' }
        ]
        response = self.client.post(self.url, visits_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(ret_obj), 2)
        self.assertEqual(ret_obj[0]['pet'], self.pet.id)
        self.assertEqual(ret_obj[1]['pet'], self.pet.id)

class PetDetailTests(BasePetClinicTest):

    def setUp(self):
        self.owner = create_owner(email='test-pet-detail@example.com')
        self.pet_type = create_pet_type('testing-pet-detail')
        self.pet = create_pet(owner=self.owner, name='fido', pet_type=self.pet_type)
        self.url = reverse('pet-detail', args=[self.pet.id])
        self.bad_url = reverse('pet-detail', args=[10000])
        self.client.credentials(HTTP_AUTHORIZATION=self.get_credentials())

    def test_retrieve_pet_by_pk(self):
        """
        Ensure a pet can be retrieved by ID
        """
        response = self.client.get(self.url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ret_obj['name'], 'fido')

    def test_retrieve_pet_by_pk_fails_bad_ID(self):
        """
        Ensure pet retrieval fails as expected for bad ID
        """
        response = self.client.get(self.bad_url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ret_obj['detail'], 'Not found.')

    def test_update_pet_by_pk(self):
        """
        Ensure pet update by ID succeeds
        """
        pet_type = create_pet_type('updated-pet-type')
        pet_data = {
            'name': 'rover', 'pet_type': pet_type.id
        }
        response = self.client.put(self.url, pet_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ret_obj['name'], 'rover')
        self.assertEqual(ret_obj['pet_type'], pet_type.id)

    def test_update_pet_by_pk_fails_bad_ID(self):
        """
        Ensure pet update fails as expected with bad ID
        """
        pet_data = {
            'name': 'rover'
        }
        response = self.client.put(self.bad_url, pet_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ret_obj['detail'], 'Not found.')

    def test_delete_pet_by_pk(self):
        """
        Ensure pet can be deleted
        """
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pet.objects.count(), 0)

    def test_delete_pet_by_pk_fails_for_bad_ID(self):
        """
        Ensure that delete fails as expected for bad ID
        """
        response = self.client.delete(self.bad_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        ret_obj = json.loads(response.content)
        self.assertEqual(ret_obj['detail'], 'Not found.')

class VisitDetailTests(BasePetClinicTest):

    def setUp(self):
        self.owner = create_owner()
        self.pet_type = create_pet_type('testing-visit')
        self.pet = create_pet(owner=self.owner, pet_type=self.pet_type)
        self.visit = create_visit(pet=self.pet)
        self.url = reverse('visit-detail', args=[self.visit.id])
        self.bad_url = reverse('visit-detail', args=[10000])
        self.client.credentials(HTTP_AUTHORIZATION=self.get_credentials())

    def test_retrieve_visit_by_pk(self):
        """
        Retrieve visit by ID
        """
        response = self.client.get(self.url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ret_obj['pet'], self.pet.id)

    def test_retrieve_visit_by_pk_fails_bad_ID(self):
        """
        Retrieve visit fails as expected for bad ID
        """
        response = self.client.get(self.bad_url, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(ret_obj['detail'], 'Not found.')

    def test_update_visit_by_pk(self):
        """
        Ensure a visit can be updaetd with ID
        """
        visit_data = {
            'description': 'new description'
        }
        response = self.client.put(self.url, visit_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ret_obj['description'], 'new description')

    def test_update_visit_by_pk_fails_with_bad_data(self):
        """
        Ensure a visit cannot be updaetd with bad date info
        """
        visit_data = {
            'visit_date': 'new description'
        }
        response = self.client.put(self.url, visit_data, format='json')
        ret_obj = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(ret_obj['visit_date'][0].startswith('Datetime has wrong format.'))

    def test_delete_visit_by_pk(self):
        """
        Ensure a visit can be deleted by ID
        """
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Visit.objects.count(), 0)

    def test_delete_visit_by_pk_fails_for_bad_ID(self):
        """
        Ensure that deleteion of visit with bad ID fails as expected
        """
        response = self.client.delete(self.bad_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
