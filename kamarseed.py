import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'percobaan3.settings')
django.setup()

from app.models import Kamars  # Import only the Kamar model

fake = Faker()

def seed_kamars(num_kamars):
    for _ in range(num_kamars):
        # Generate fake data for each field
        nomor_kamar = fake.random_int(min=100, max=999)
        status_kamar = 'Tersedia'  # You can set the status here

        # Create an instance of the Kamars model and populate its fields with fake data
        kamar = Kamars(
            nomor_kamar=nomor_kamar,
            status_kamar=status_kamar,
        )
        kamar.save()

if __name__ == '__main__':
    num_kamars = 100  # Specify the number of Kamars you want to create
    seed_kamars(num_kamars)
