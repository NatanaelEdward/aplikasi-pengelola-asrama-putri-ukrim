import os
import django
import random
import datetime
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'percobaan3.settings')
django.setup()

from app.models import Mahasiswas, Kamars, Pendaftarans  # Replace with your actual models

fake = Faker()

def seed_database(num_records):
    tersedia_kamars = Kamars.objects.filter(status_kamar='Tersedia')
    num_tersedia_kamars = tersedia_kamars.count()

    if num_tersedia_kamars < num_records:
        raise ValueError("Insufficient 'Tersedia' kamars available for seeding.")

    kamars_sample = random.sample(list(tersedia_kamars), num_records)

    for i in range(num_records):
        # Generate fake data for each field
        nim = '214210' + str(fake.random_int(min=1000, max=9999))
        nama = fake.name()
        jurusan = random.choice([choice[0] for choice in Mahasiswas.PILIHAN_JURUSAN])
        no_telepon = fake.random_number(digits=10)
        tempat_lahir = fake.city()
        tanggal_lahir = fake.date_of_birth(minimum_age=18, maximum_age=30)
        nomor_kamar = kamars_sample[i]

        # Create an instance of the Mahasiswas model and populate its fields with fake data
        record = Mahasiswas(
            nim=nim,
            nama=nama,
            jurusan=jurusan,
            no_telepon=no_telepon,
            tempat_lahir=tempat_lahir,
            tanggal_lahir=tanggal_lahir,
            nomor_kamar=nomor_kamar,
        )
        record.save()

        # Create a Pendaftaran object for the Mahasiswa
        pendaftaran = Pendaftarans(
            tanggal_daftar=datetime.date.today(),
            nim=record,
        )
        pendaftaran.save()

        # Update the nim field of the associated nomor_kamar to the newly created Mahasiswa
        nomor_kamar.nim = record
        nomor_kamar.status_kamar = 'Terpakai'
        nomor_kamar.save()

if __name__ == '__main__':
    num_records = 10  # Specify the number of records you want to create
    seed_database(num_records)
