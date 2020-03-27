from django.core.management.base import BaseCommand, CommandError
from petclinic.models import Owner, Pet, PetType, Vet, Specialty, Visit
from faker import Faker
fake = Faker()
import random

class Command(BaseCommand):
    help = 'Populates the petclinic database with fake sample data for development work'

    def add_arguments(self, parser):
        parser.add_argument(
            '-o',
            '--owners',
            help='number of owners to create, default 100',
            type=int
        )
        parser.add_argument(
            '--vets',
            help='number of vets to create, default 50',
            type=int
        )

    def handle(self, *args, **options):        
        self.owner_count = options['owners'] if options['owners'] else 100
        self.vet_count = options['vets'] if options['vets'] else 50
        self.populate()
        self.stdout.write(self.style.SUCCESS('Database populated'))

    def populate(self):
        self.stdout.write(self.style.SUCCESS('Owners: ' + str(self.owner_count)))
        self.stdout.write(self.style.SUCCESS('Vets: ' + str(self.vet_count)))
        self.clean_up_db()
        self.create_pet_types()
        self.create_specialties()
        self.create_vets()
        self.stdout.write(self.style.SUCCESS('PetType count: ' + str(PetType.objects.count())))
        self.stdout.write(self.style.SUCCESS('Specialty count: ' + str(Specialty.objects.count())))
        self.stdout.write(self.style.SUCCESS('Vet count: ' + str(Vet.objects.count())))


    def clean_up_db(self):
        PetType.objects.all().delete()
        Specialty.objects.all().delete()
        Vet.objects.all().delete()

    def create_pet_types(self):
        pet_type_list = ['bird','cat','dog','fish','hamster','horse','iguana',        
                        'lizard','mouse','pig','rabbit','rat','snake','snake',
                        'tortoise','turtle']
        self.pet_types = []
        for pt in pet_type_list:
            pet_type = PetType.objects.create(name=pt)
            self.pet_types.append(pet_type)

    def create_specialties(self):
        specialty_list = ['dentistry','dermatology','emergency','imaging',
                        'radiology','surgery','vision']
        self.specialties = []
        for sp in specialty_list:
            specialty = Specialty.objects.create(name=sp)
            self.specialties.append(specialty)

    def create_vets(self):
        self.vets = []
        for i in range(0, self.vet_count):
            specialty = self.specialties[random.randrange(len(self.specialties))]
            vet = Vet.objects.create(
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                street_address=fake.street_address(),
                city=fake.city(),
                state=fake.state_abbr(),
                telephone=fake.phone_number(),
                specialty=specialty
            )
            self.vets.append(vet)
