# Generated by Django 4.1.5 on 2023-04-24 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_kamars_nomor_kamar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kamars',
            name='nomor_kamar',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
