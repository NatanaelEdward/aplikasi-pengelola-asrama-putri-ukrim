# Generated by Django 4.1.5 on 2023-04-24 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_mahasiswas_jurusan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mahasiswas',
            name='metode_pembayaran',
        ),
    ]
