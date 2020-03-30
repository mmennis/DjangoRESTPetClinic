from django.test import TestCase
from rest_framework.renderers import JSONRenderer

from petclinic.models import Owner, Pet, PetType, Specialty, Vet, Visit
from petclinic.serializers import *
from petclinic.test_utils import *


class OwnerSerializerTest(TestCase):

    def setUp(self):
        self.owner = create_owner(email='serializer@example.com')
        self.pet_type = create_pet_type(pet_type_name='doggy')
        self.pet = create_pet(owner=self.owner)
        self.serializer = OwnerSerializer(instance=self.owner)

    def test_expected_owner_fields_present(self):
        data = self.serializer.data
        self.assertEqual(data.keys(), 
                set(['id', 'email','first_name', 'last_name', 'street_address', 'city',
                        'state', 'telephone', 'pets'
                ]))

    def test_contains_expected_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['email'], 'serializer@example.com')
        self.assertEqual(data['id'], self.owner.id)

    def test_contains_expected_pet_fields(self):
        data = self.serializer.data
        pet_data = data['pets']
        self.assertEqual(len(pet_data), 1)
        self.assertEqual(pet_data[0].keys(), 
                set(['id','name', 'owner', 'birth_date','pet_type','visits']))

    def test_contains_expected_field_content(self):
        data = self.serializer.data
        self.assertEqual(len(data['pets']), 1)
        pet_data = data['pets'][0]
        self.assertEqual(pet_data['id'], self.pet.id)
        self.assertEqual(pet_data['owner'], self.owner.id)

class VetSerializerTest(TestCase):

    def setUp(self):
        self.specialty = create_specialty('specialty_test')
        self.vet = create_vet(specialty=self.specialty, email='vet-serializer-test@example.com')
        self.serializer = VetSerializer(instance=self.vet)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(data.keys(), 
                    set(['id','first_name','last_name','city','state','street_address',
                            'specialty','email','telephone'
                    ]))

    def test_contains_expected_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.vet.id)
        self.assertEqual(data['email'], 'vet-serializer-test@example.com')
        self.assertEqual(data['specialty'], self.specialty.id)

class PetTypeSerializerTest(TestCase):

    def setUp(self):
        self.pet_type = create_pet_type(pet_type_name='frog')
        self.serializer = PetTypeSerializer(instance=self.pet_type)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(data.keys(), set(['id', 'name']))

    def test_contains_expected_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.pet_type.id)
        self.assertEqual(data['name'], 'frog')

class SpecialtySerializerTest(TestCase):

    def setUp(self):
        self.specialty = create_specialty(specialty_name='serializer-testing')
        self.serializer = SpecialtySerializer(instance=self.specialty)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(data.keys(), set(['id', 'name']))

    def test_contains_expected_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.specialty.id)
        self.assertEqual(data['name'], 'serializer-testing')

class PetSerializerTest(TestCase):

    def setUp(self):
        self.owner = create_owner(email='pet-serializer-test@example.com')
        self.pet = create_pet(owner=self.owner)
        self.serializer = PetSerializer(instance=self.pet)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(data.keys(), set(['id','birth_date','owner','name','visits','pet_type']))

    def test_contains_expected_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.pet.id)
        self.assertEqual(data['owner'], self.owner.id)
        self.assertEqual(len(data['visits']), 0)

class VisitSerializerTest(TestCase):

    def setUp(self):
        self.owner = create_owner()
        self.pet = create_pet(owner=self.owner)
        self.visit = create_visit(pet=self.pet)
        self.serializer = VisitSerializer(instance=self.visit)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(data.keys(), set(['id','visit_date','description','pet']))

    def test_contains_expected_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id'], self.visit.id)
        self.assertEqual(data['pet'], self.pet.id)
