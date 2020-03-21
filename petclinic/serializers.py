from rest_framework import serializers

from petclinic.models import Owner, Pet, PetType, Vet, Visit


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['id', 'visit_date', 'description']

class PetSerializer(serializers.ModelSerializer):
    visits = VisitSerializer(many=True, read_only=True)
    pet_type = serializers.StringRelatedField(many=False)
    class Meta:
        model = Pet
        fields = ['id', 'name', 'pet_type', 'visits']

class OwnerSerializer(serializers.ModelSerializer):
    pets = PetSerializer(many=True, read_only=True)
    class Meta:
        model = Owner
        fields = ['id', 'email', 'first_name', 'last_name', 'street_address', 'city', 'state', 'telephone', 'pets']

class VetSerializer(serializers.ModelSerializer):
    specialty = serializers.StringRelatedField(many=False)
    class Meta:
        model = Vet
        fields = ['id', 'email', 'first_name', 'last_name', 'street_address', 'city', 'state', 'telephone', 'specialty']
