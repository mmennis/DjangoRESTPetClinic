import datetime

from django.test import TestCase
from django.utils import timezone
from rest_framework.renderers import JSONRenderer

from petclinic.models import Owner, Pet, PetType, Specialty, Vet, Visit


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

def create_pet(name='fido', owner=None, birth_date=None):
    bd = (timezone.now() - datetime.timedelta(days=10)) if birth_date is None else birth_date
    pt = create_pet_type('dog')
    return Pet.objects.create(name=name, birth_date=bd, pet_type=pt, owner=owner)

def create_visit(visit_date=timezone.now(), description='Visit description', pet=None):
    return Visit.objects.create(visit_date=visit_date, description=description, pet=pet)
