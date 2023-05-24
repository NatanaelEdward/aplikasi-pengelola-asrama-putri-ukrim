# seed.py
import os
import django
import random
import datetime
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'percobaan3.settings')
django.setup()

from app.models import Mahasiswas, Kamars  # Replace with your actual models

fake = Faker()

def seed_database(num_records):
    for _ in range(num_records):
        # Generate fake data for each field
        nim = fake.random_int(min=10000, max=99999)
        nama = fake.name()
        jurusan = random.choice([choice[0] for choice in Mahasiswas.PILIHAN_JURUSAN])
        no_telepon = fake.random_number(digits=10)
        tempat_lahir = fake.city()
        tanggal_lahir = fake.date_of_birth(minimum_age=18, maximum_age=30)
        nomor_kamar = random.choice(Kamars.objects.all())

        # Create an instance of the Mahasiswas model and populate its fields with fake data
        record = Mahasiswas(
            nim=str(nim),
            nama=nama,
            jurusan=jurusan,
            no_telepon=no_telepon,
            tempat_lahir=tempat_lahir,
            tanggal_lahir=tanggal_lahir,
            nomor_kamar=nomor_kamar,
        )
        record.save()

if __name__ == '__main__':
    num_records = 10  # Specify the number of records you want to create
    seed_database(num_records)
