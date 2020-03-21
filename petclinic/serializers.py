from rest_framework import serializers

from petclinic.models import Owner, Pet, PetType, Vet, Visit


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['id', 'visit_date', 'description', 'date_created', 'date_modified']

class PetSerializer(serializers.ModelSerializer):
    visits = VisitSerializer(many=True, read_only=True)
    pet_type = serializers.StringRelatedField(many=False)
    class Meta:
        model = Pet
        fields = ['id', 'name', 'pet_type', 'visits', 'date_created', 'date_modified']

class OwnerSerializer(serializers.ModelSerializer):
    pets = PetSerializer(many=True, read_only=True)
    class Meta:
        model = Owner
        fields = ['id', 'email', 'first_name', 'last_name', 'street_address', 'city', 'state', 'telephone', 'pets', 'date_created', 'date_modified']

class VetSerializer(serializers.ModelSerializer):
    specialty = serializers.StringRelatedField(many=False)
    class Meta:
        model = Vet
        fields = ['id', 'email', 'first_name', 'last_name', 'street_address', 'city', 'state', 'telephone', 'specialty', 'date_created', 'date_modified']
