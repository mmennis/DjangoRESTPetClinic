import datetime
from django.utils import timezone
from django.test import TestCase
from petclinic.models import Specialty, Vet, PetType, Pet, Owner

# Create your tests here.
def create_specialty(specialty_name):
    s = Specialty()
    s.name = specialty_name
    s.save()
    return s

def create_pet_type(pet_type_name):
    return PetType.objects.create(name=pet_type_name)

def create_vet(email='test@example.com', first_name='First', 
                last_name='Last', street_address='1234 Main St', 
                city='San Jose', state='CA', telephone='408-555-1212'):
    specialty = create_specialty('testing')
    return Vet.objects.create(email=email, first_name=first_name, last_name=last_name, 
                                street_address=street_address, telephone=telephone, 
                                specialty=specialty)

def create_owner(email='test@example.com', first_name='First', last_name='Last', 
                    street_address='1234 Main St', city='San Jose', state='CA', 
                    telephone='408-555-1212'):
    return Owner.objects.create(email=email, first_name=first_name, last_name=last_name, 
                                street_address=street_address, telephone=telephone)

def create_pet(name='fido', owner=None):
    bd = timezone.now() - datetime.timedelta(days=10)
    pt = create_pet_type('dog')
    return Pet.objects.create(name=name, birth_date=bd, pet_type=pt, owner=owner)

class VetModelTest(TestCase):

    def test_should_create_a_vet(self):
        """
        A vet should be created and persisted
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

    def test_should_create_a_pet(self):
        """
        A pet should be created
        """
        o = create_owner(email='test3@example.com')
        p = create_pet(owner=o)
        self.assertIsInstance(p, Pet)

    def test_should_persist_a_pet(self):
        """
        Pet should be written to database
        """
        o = create_owner(email='test1@example.com')
        p = create_pet(owner=o)
        self.assertIn(p, o.pet_set.all())
        self.assertEqual(o.pet_set.count(), 1)
        self.assertIn(p, Pet.objects.all())


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

