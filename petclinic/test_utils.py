import datetime
import json

from django.test import TestCase
from django.utils import timezone
from rest_framework.renderers import JSONRenderer

from petclinic.models import (Owner, Pet, PetType, Specialty, User,
                              UserProfile, Vet, Visit)


# Create your tests here.
def create_user(email='test_user@example.com', username='test_user', 
                password='test_passwd_123', last_name='Last', first_name='First'):
    user = User.objects.create_user(username=username, email=email, password=password, 
                                    last_name=last_name, first_name=first_name, is_active=True)
    return user

def create_user_profile(user):
    user_profile = UserProfile.objects.create(user=user, title='Mr', dob=timezone.now().date(),
                                                address='123 Main St', country='USA', city='San Jose',
                                                zip='95050')
    return user_profile

def create_specialty(specialty_name):
    s = Specialty()
    s.name = specialty_name
    s.save()
    return s

def create_pet_type(pet_type_name):
    return PetType.objects.create(name=pet_type_name)

def create_vet(email='test@example.com', first_name='First', 
                last_name='Last', street_address='1234 Main St', 
                city='San Jose', state='CA', telephone='408-555-1212',
                specialty=None):
    specialty = create_specialty('testing') if specialty is None else specialty
    return Vet.objects.create(email=email, first_name=first_name, last_name=last_name, 
                                street_address=street_address, telephone=telephone, 
                                specialty=specialty, city=city, state=state)

def create_owner(email='test@example.com', first_name='First', last_name='Last', 
                    street_address='1234 Main St', city='San Jose', state='CA', 
                    telephone='408-555-1212'):
    return Owner.objects.create(email=email, first_name=first_name, last_name=last_name, 
                                street_address=street_address, telephone=telephone, state=state,
                                city=city)

def create_pet(name='fido', owner=None, birth_date=None, pet_type=None):
    bd = (timezone.now() - datetime.timedelta(days=10)).date() if birth_date is None else birth_date
    return Pet.objects.create(name=name, birth_date=bd, pet_type=pet_type, owner=owner)

def create_visit(visit_date=timezone.now(), description='Visit description', pet=None):
    return Visit.objects.create(visit_date=visit_date, description=description, pet=pet)
