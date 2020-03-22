from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from petclinic.models import Owner, Pet, Vet, Visit, Specialty, PetType
from petclinic.serializers import (OwnerSerializer, PetSerializer,
                                   VetSerializer, VisitSerializer, SpecialtySerializer)


class OwnerList(APIView):
    """
    List all owners, or create a new owner
    """
    def get(self, request, format=None):
        owners = Owner.objects.all()
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
