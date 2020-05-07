from rest_framework import serializers

from petclinic.models import Owner, Pet, PetType, Specialty, Vet, Visit, User, UserProfile


class PetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetType
        fields = ['id', 'name']
        read_only_fields = ('date_created', 'date_modified')

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'name']
        read_only_fields = ('date_created', 'date_modified')

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['id', 'visit_date', 'description', 'pet']
        read_only_fields = ('date_created', 'date_modified')

class PetSerializer(serializers.ModelSerializer):
    visits = VisitSerializer(many=True, read_only=True)
    pet_type = serializers.PrimaryKeyRelatedField(queryset=PetType.objects.all())
    class Meta:
        model = Pet
        fields = ['id', 'name', 'pet_type', 'visits', 'birth_date', 'owner']
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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['title', 'dob', 'address', 'country', 'city', 'zip', 'photo']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ['url', 'email', 'first_name', 'last_name', 'password', 'profile']
        extra_kwargs = { 'password': { 'write_only': True } }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.title = profile_data.get('title', profile.title)
        profile.dob = profile_data.get('dob', profile.dob)
        profile.address = profile_data.get('address', profile.address)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.zip = profile_data.get('zip', profile.zip)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.save()
        return instance
