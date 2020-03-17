from django.db import models
from django.core.validators import validate_email

# Owner
class Owner(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50, db_index=True)
    state = models.CharField(max_length=50, db_index=True)
    telephone = models.CharField(max_length=30)
    email = models.EmailField(unique=True, max_length=100, validators=[validate_email])

# Visit
class Visit(models.Model):
    visit_date = models.DateTimeField()
    description = models.TextField(max_length=256,  blank=True, default='check up')

# Pet Type
class PetType(models.Model):
    name = models.CharField(max_length=30, unique=True)

# Pet
class Pet(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    birth_date = models.DateField()
    pet_type = models.ForeignKey(PetType, on_delete=models.SET_NULL)
    visits = models.ForeignKey(Visit, on_delete=models.CASCADE)

class Specialty(models.Model):
    name = models.CharField(max_length=30, default='general practice')

# Vet
class Vet(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50, db_index=True)
    state = models.CharField(max_length=50, db_index=True)
    telephone = models.CharField(max_length=30)
    specialty = models.ManyToManyField(Specialty)


