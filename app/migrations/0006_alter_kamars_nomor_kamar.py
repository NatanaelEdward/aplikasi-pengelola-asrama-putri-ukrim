# Generated by Django 4.1.5 on 2023-04-24 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_mahasiswas_tempat_lahir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kamars',
            name='nomor_kamar',
            field=models.CharField(auto_created=True, default='1', max_length=113, primary_key=True, serialize=False),
        ),
    ]