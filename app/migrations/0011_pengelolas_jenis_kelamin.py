# Generated by Django 4.1.5 on 2023-05-26 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_pengelolas_tempat_lahir'),
    ]

    operations = [
        migrations.AddField(
            model_name='pengelolas',
            name='jenis_kelamin',
            field=models.CharField(choices=[('Laki-laki', 'laki-laki'), ('Perempuan', 'perempuan')], default=None, max_length=20),
        ),
    ]
