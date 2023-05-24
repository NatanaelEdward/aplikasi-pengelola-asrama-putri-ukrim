# Generated by Django 4.1.5 on 2023-04-24 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_pendaftarans_pengelola'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mahasiswas',
            name='jurusan',
            field=models.CharField(choices=[('Informatika', 'Informatika'), ('Manajemen', 'Manajemen'), ('Farmasi', 'Farmasi'), ('Pendidikan Agama Kristen', 'Pendidikan Agama Kristen'), ('Fisika', 'Fisika'), ('Teologi Konseling Kristen', 'Teologi Konseling Kristen'), ('Akuntansi', 'Akuntansi'), ('Teknik Sipil', 'Teknik Sipil'), ('Musik Gereja', 'Musik Gereja')], default='Farmasi', max_length=50),
        ),
    ]
