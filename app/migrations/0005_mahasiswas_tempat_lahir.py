# Generated by Django 4.1.5 on 2023-04-24 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_mahasiswas_metode_pembayaran'),
    ]

    operations = [
        migrations.AddField(
            model_name='mahasiswas',
            name='tempat_lahir',
            field=models.CharField(default=None, max_length=255),
        ),
    ]