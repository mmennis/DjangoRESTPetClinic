from django.db import models
from django.utils import timezone

# Owner
class Owner(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    telephone = models.CharField(max_length=100)

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return "%s, %s" % (self.full_name(), self.email)

# Specialty
class Specialty(models.Model):
    name: models.CharField(max_length=30, unique=True, null=False)

    def __str__(self):
        return self.name

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

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return "%s, %s" % (self.full_name(), self.email)

    
# Pet Type
class PetType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

# Pet
class Pet(models.Model):
    name = models.CharField(max_length=30, blank=False)
    birth_date = models.DateField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    pet_type = models.ForeignKey(PetType, null=True, on_delete=models.SET_NULL,)


    def age(self):
        """
        return a timedelta object for curent age
        """
        return timezone.now() - self.birth_date

    def __str__(self):
        return ("%s aged ")

# Visit
class Visit(models.Model):
    visit_date = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=1000)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)


