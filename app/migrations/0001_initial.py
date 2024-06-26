# Generated by Django 4.1.5 on 2023-04-20 06:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kamars',
            fields=[
                ('nomor_kamar', models.CharField(auto_created=True, default='1', max_length=10, primary_key=True, serialize=False)),
                ('status_kamar', models.CharField(choices=[('TERSEDIA', 'Tersedia'), ('TERPAKAI', 'Terpakai')], default='Tersedia', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Mahasiswas',
            fields=[
                ('nim', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=255)),
                ('jurusan', models.CharField(choices=[('Informatika', 'Informatika'), ('Manajemen', 'Manajemen'), ('Farmasi', 'Farmasi')], default='Farmasi', max_length=20)),
                ('no_telepon', models.CharField(max_length=20)),
                ('tanggal_lahir', models.DateField(default=datetime.date.today)),
                ('metode_pembayaran', models.CharField(choices=[('Qris', 'Qris'), ('Cash', 'Cash')], default='Qris', max_length=20)),
                ('nomor_kamar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.kamars')),
            ],
        ),
        migrations.CreateModel(
            name='Pengelolas',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nama', models.CharField(max_length=255)),
                ('tanggal_lahir', models.DateField(default=datetime.date.today)),
                ('alamat', models.TextField()),
                ('no_telepon', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Pendaftarans',
            fields=[
                ('id_pendaftaran', models.AutoField(primary_key=True, serialize=False)),
                ('tanggal_daftar', models.DateField(default=datetime.date.today)),
                ('tanggal_masuk', models.DateField(blank=True, default=None, null=True)),
                ('tanggal_keluar', models.DateField(blank=True, default=None, null=True)),
                ('bukti_bayar', models.ImageField(blank=True, upload_to='bukti_bayar/')),
                ('nim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.mahasiswas')),
            ],
        ),
        migrations.AddField(
            model_name='kamars',
            name='nim',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.mahasiswas'),
        ),
    ]
