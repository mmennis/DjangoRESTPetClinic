from django.db import models

# Owner
class Owner(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    telephone = models.CharField(max_length=100)

# Specialty
class Specialty(models.Model):
    name: models.CharField(max_length=30, unique=True)

# Vet
class Vet(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    telephone = models.CharField(max_length=100)  
    specialty = models.ForeignKey(Specialty, null=True, on_delete=models.SET_NULL)
    
# Pet Type
class PetType(models.Model):
    name = models.CharField(max_length=32)

# Pet
class Pet(models.Model):
    name = models.CharField(max_length=30, blank=False)
    birth_date = models.DateField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    pet_type = models.ForeignKey(PetType, null=True, on_delete=models.SET_NULL,)

# Visit
class Visit(models.Model):
    visit_date = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=1000)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)


