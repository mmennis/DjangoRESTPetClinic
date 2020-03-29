from django.http import Http404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from petclinic.models import Owner, Pet, Vet, Visit, Specialty, PetType
from petclinic.serializers import (OwnerSerializer, PetSerializer,
                                   VetSerializer, VisitSerializer, 
                                   SpecialtySerializer, PetTypeSerializer)


class OwnerList(APIView):
    """
    List all owners, or create a new owner
    """
    def get(self, request, format=None):
        owners = Owner.objects.all()
        state = request.query_params.get('state', None)
        if state is not None:
            owners = owners.filter(state=state)
        serializer = OwnerSerializer(owners, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OwnerDetail(APIView):
    """
    Retrive, update or delete a specific owner instance
    """
    def get_object(self, pk):
        try:
            return Owner.objects.get(pk=pk)
        except Owner.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        owner = self.get_object(pk)
        serializer = OwnerSerializer(owner)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        owner = self.get_object(pk)
        serializer = OwnerSerializer(owner, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        owner = self.get_object(pk)
        owner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VetList(APIView):
    """
    List all vets or create a new vet
    """
    def get(self, request, format=None):
        vets = Vet.objects.all()
        state = request.query_params.get('state', None)
        if state is not None:
            vets = vets.filter(state=state)
        serializer = VetSerializer(vets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VetDetail(APIView):
    """
    Retrieve, update or delete specific instances of a vet
    """
    def get_object(self, pk):
        try:
            return Vet.objects.get(pk=pk)
        except Vet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        vet = self.get_object(pk)
        serializer = VetSerializer(vet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        vet = self.get_object(pk)
        serializer = VetSerializer(vet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vet = self.get_object(pk)
        vet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    

class SpecialtyList(APIView):
    """
    List all specialties
    """
    def get(self, request, format=None):
        specialties = Specialty.objects.all()
        serializer = SpecialtySerializer(specialties, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SpecialtySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecialtyDetail(APIView):
    """
    Retrieve, update a speciality (delete blocked)
    """
    def get_object(self, pk):
        try:
            return Specialty.objects.get(pk=pk)
        except Specialty.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        specialty = self.get_object(pk)
        serializer = SpecialtySerializer(specialty)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        specialty = self.get_object(pk)
        serializer = SpecialtySerializer(specialty, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.erors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        data = { 'message': 'Unsupported operation'}
        return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class PetTypeList(APIView):
    """
    List all or create a new pet types
    """
    def get(self, request, format=None):
        pet_types = PetType.objects.all()
        serializer = PetTypeSerializer(pet_types, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PetTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PetTypeDetail(APIView):
    """
    Retrieve, update a pet type (delete blocked)
    """
    def get_object(self, pk):
        try:
            return PetType.objects.get(pk=pk)
        except PetType.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pet_type = self.get_object(pk)
        serializer = PetTypeSerializer(pet_type)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        pet_type = self.get_object(pk)
        serializer = PetTypeSerializer(pet_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        data = { 'message': 'Unsupported operation'}
        return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class OwnerPetList(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def get_queryset(self):
        owner_pk = self.kwargs['owner_pk']
        return self.queryset.filter(owner=owner_pk)

    def pre_save(self, obj):
        obj.owner = self.kwargs['owner_pk']

    def create(self, request, *args, **kwargs):
        owner_id = self.kwargs['owner_pk']
        for pet_data in request.data:
            pet_data['owner'] = owner_id
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        pets_created = []
        for pet_data in request.data:
            pet_data['owner'] = Owner.objects.get(pk=owner_id)
            pet_data['pet_type'] = PetType.objects.get(pk=pet_data['pet_type'])
            pet = Pet(**pet_data)
            pet.save()
            pets_created.append(pet.id)
        results = Pet.objects.filter(id__in=pets_created)
        output_serializer = PetSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data, status=status.HTTP_201_CREATED)

class PetVisitList(generics.ListCreateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

    def get_queryset(self):
        pet_pk = self.kwargs['pet_pk']
        return self.queryset.filter(pet=pet_pk)

    def pre_save(self, obj):
        obj.pet = self.kwargs['pet_pk']

    def create(self, request, *args, **kwargs):
        pet_id = self.kwargs['pet_pk']
        for visit_data in request.data:
            visit_data['pet'] = pet_id
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        visits_created = []
        for visit_data in request.data:
            visit_data['pet'] = Pet.objects.get(pk=pet_id)
            visit = Visit.objects.create(**visit_data)
            visits_created.append(visit.id)
        results = Visit.objects.filter(id__in=visits_created)
        output_serializer = VisitSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data, status=status.HTTP_201_CREATED)

