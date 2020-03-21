from django.test import TestCase
from petclinic.models import Specialty, Vet, PetType, Pet, Owner, Visit
from petclinic.test_utils import *
from petclinic.serializers import OwnerSerializer, PetSerializer
from rest_framework.renderers import JSONRenderer

class OwnerSerializerTest(TestCase):

    def test_the_serializer_should_do_something(self):
        owner = create_owner(email='serializer@example.com')
        pet_type = create_pet_type(pet_type_name='doggy')
        pet = create_pet(owner=owner)
        visit = create_visit(pet=pet)
        visit2 = create_visit(pet=pet)
        o_szer = OwnerSerializer(instance=owner)
        content = JSONRenderer().render(o_szer.data)
        #print(content)