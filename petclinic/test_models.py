import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from petclinic.models import Owner, Pet, PetType, Specialty, Vet, Visit, User, UserProfile
from petclinic.test_utils import *

from rest_framework.test import APITestCase

class UserModelTest(APITestCase):
    def test_should_create_a_user(self):
        """
        A new user should be created
        """
        user = create_user()
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test_user@example.com')

    def test_user_should_login(self):
        user = create_user()
        login = self.client.login(email='test_user@example.com', password='test_passwd_123')
        self.assertTrue(login)

class UserProfileModelTest(TestCase):
    pass

class VetModelTest(TestCase):

    def test_should_create_a_vet(self):
        """
        A vet should be created
        """
        vet = create_vet()
        self.assertIsInstance(vet, Vet)
        self.assertEqual(vet.full_name(), 'First Last')
        self.assertEqual(vet.specialty.name, 'testing')

    def test_should_persist_a_vet(self):
        """
        Vet should be persisted to the db
        """
        vet = create_vet()
        vets = Vet.objects.all()
        self.assertIn(vet, vets)


class PetModelTest(TestCase):
    
    def setUp(self):
        self.owner = create_owner(email='testing-pet@example.com')

    def test_should_create_a_pet(self):
        """
        A pet should be created
        """        
        p = create_pet(owner=self.owner)
        self.assertIsInstance(p, Pet)

    def test_should_persist_a_pet(self):
        """
        Pet should be written to database
        """
        p = create_pet(owner=self.owner)
        self.assertIn(p, self.owner.pets.all())
        self.assertEqual(self.owner.pets.count(), 1)
        self.assertIn(p, Pet.objects.all())

    def test_should_report_pets_age(self):
        bd = timezone.now() - datetime.timedelta(days=90)
        p = create_pet(owner=self.owner, birth_date=bd)
        self.assertEqual(p.age().days, 90)

    def test_should_add_a_visit(self):
        """
        adding a pet to a visit should appear in visit_set of pet
        """
        p = create_pet(owner = self.owner)
        v = create_visit(pet=p)
        self.assertIn(v, p.visits.all())


class OwnerModelTest(TestCase):

    def test_should_create_an_owner(self):
        """
        An owner should be created
        """
        o = create_owner()
        self.assertIsInstance(o, Owner)
        self.assertRegex("%s" %o, o.email)

    def test_should_persist_an_owner(self):
        """
        An owner should be persisted in db
        """
        o = create_owner()        
        owners = Owner.objects.all()
        self.assertIn(o, owners)

class VisitModelTest(TestCase):

    def setUp(self):
        self.owner = create_owner(email='testing-visit@example.com')
        self.pet = create_pet(owner=self.owner)

    def test_should_create_a_visit(self):
        """
        a visit should be created
        """
        v = create_visit(pet=self.pet)
        self.assertIsInstance(v, Visit)

    def test_should_add_visit_to_pet_visit_set(self):
        """
        a visit should appear in a pets list of visits
        """
        v = create_visit(pet=self.pet)
        self.assertIn(v, self.pet.visits.all())
