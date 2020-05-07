from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _ 
from django.conf import settings

# User
class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=5)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='uploads', blank=True)



# Owner
class Owner(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    telephone = models.CharField(max_length=100)
    date_created = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """
        On save update timestamps
        """
        if not self.id:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        return super(Owner, self).save(*args, **kwargs)

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return "%s, %s" % (self.full_name(), self.email)

# Specialty
class Specialty(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    date_created = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """
        On save update timestamps
        """
        if not self.id:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        return super(Specialty, self).save(*args, **kwargs)

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
    specialty = models.ForeignKey(Specialty, null=True, on_delete=models.SET_NULL, related_name='vets')
    date_created = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """
        On save update timestamps
        """
        if not self.id:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        return super(Vet, self).save(*args, **kwargs)

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return "%s, %s" % (self.full_name(), self.email)

    
# Pet Type
class PetType(models.Model):
    name = models.CharField(max_length=32, unique=True)
    date_created = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """
        On save update timestamps
        """
        if not self.id:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        return super(PetType, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# Pet
class Pet(models.Model):
    name = models.CharField(max_length=30, blank=False)
    birth_date = models.DateField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='pets')
    pet_type = models.ForeignKey(PetType, null=True, on_delete=models.SET_NULL, related_name='pets')
    date_created = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """
        On save update timestamps
        """
        if not self.id:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        return super(Pet, self).save(*args, **kwargs)

    # FIXME
    def age(self):
        """
        return a timedelta object for curent age
        """
        return timezone.now() - self.birth_date

    def __str__(self):
        # return ("%s aged %s" % (self.name, self.age().years()))
        return self.name

# Visit
class Visit(models.Model):
    visit_date = models.DateTimeField()
    description = models.TextField(max_length=1000)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='visits')
    date_created = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """
        On save update timestamps
        """
        if not self.id:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        return super(Visit, self).save(*args, **kwargs)
