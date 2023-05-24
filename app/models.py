from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
import datetime
# Create your models here.



class Kamars(models.Model):
    PILIHAN_KAMAR = (('TERSEDIA', 'Tersedia'), ('TERPAKAI', 'Terpakai'))

    nomor_kamar = models.IntegerField(primary_key=True, auto_created=True)
    status_kamar = models.CharField(
        max_length=8, choices=PILIHAN_KAMAR, default='Tersedia')
    nim = models.OneToOneField(
        'Mahasiswas', on_delete=models.SET_NULL, null=True, blank=True)

class Mahasiswas(models.Model):

    PILIHAN_JURUSAN = (
        ("Informatika", "Informatika"),
        ("Manajemen", "Manajemen"),
        ("Farmasi", "Farmasi"),
        ("Pendidikan Agama Kristen","Pendidikan Agama Kristen"),
        ("Fisika","Fisika"),
        ("Teologi Konseling Kristen","Teologi Konseling Kristen"),
        ("Akuntansi","Akuntansi"),
        ("Teknik Sipil","Teknik Sipil"),
        ("Musik Gereja","Musik Gereja"),
    )

    PILIHAN_PEMBAYARAN = (
        ("Qris", "Qris"),
        ("Cash", "Cash")
    )

    nim = models.CharField(max_length=10, primary_key=True)
    nama = models.CharField(max_length=255)
    jurusan = models.CharField(max_length=50,
                               choices=PILIHAN_JURUSAN,
                               default="Farmasi")
    no_telepon = models.CharField(max_length=20)
    tempat_lahir = models.CharField(max_length=255, default=None)
    tanggal_lahir = models.DateField(default=datetime.date.today)
    nomor_kamar = models.ForeignKey(
        Kamars, on_delete=models.SET_NULL, null=True, blank=True)

class Pengelolas(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    nama = models.CharField(max_length=255)
    tanggal_lahir = models.DateField(default=datetime.date.today)
    alamat = models.TextField()
    no_telepon = models.CharField(max_length=15)

class Pendaftarans(models.Model):
    id_pendaftaran = models.AutoField(primary_key=True)
    tanggal_daftar = models.DateField(default=datetime.date.today)
    tanggal_masuk = models.DateField(default=None, null=True, blank=True)
    tanggal_keluar = models.DateField(default=None, null=True, blank=True)
    bukti_bayar = models.ImageField(upload_to='bukti_bayar/',blank=True)
    nim = models.ForeignKey(Mahasiswas, on_delete=models.CASCADE)
    pengelola = models.ForeignKey(Pengelolas, on_delete=models.CASCADE, null=True, blank=True)