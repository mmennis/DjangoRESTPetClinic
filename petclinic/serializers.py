from rest_framework import serializers

from petclinic.models import Owner, Pet, PetType, Vet, Visit, Specialty


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['id', 'visit_date', 'description']
        read_only_fields = ('date_created', 'date_modified')

class PetSerializer(serializers.ModelSerializer):
    visits = VisitSerializer(many=True, read_only=True)
    pet_type = serializers.PrimaryKeyRelatedField(queryset=PetType.objects.all())
    class Meta:
        model = Pet
        fields = ['id', 'name', 'pet_type', 'visits']
        read_only_fields = ('date_created', 'date_modified')

class OwnerSerializer(serializers.ModelSerializer):
    pets = PetSerializer(many=True, read_only=True)
    class Meta:
        model = Owner
        fields = ['id', 'email', 'first_name', 'last_name', 'street_address', 'city', 'state', 'telephone', 'pets']
        read_only_fields = ('date_created', 'date_modified')

class VetSerializer(serializers.ModelSerializer):
    specialty = serializers.PrimaryKeyRelatedField(queryset=Specialty.objects.all())
    class Meta:
        model = Vet
        fields = ['id', 'email', 'first_name', 'last_name', 'street_address', 'city', 'state', 'telephone', 'specialty']
        read_only_fields = ('date_created', 'date_modified')
    
