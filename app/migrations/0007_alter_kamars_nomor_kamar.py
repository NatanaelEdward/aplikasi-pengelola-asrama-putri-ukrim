# Generated by Django 4.1.5 on 2023-04-24 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_kamars_nomor_kamar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kamars',
            name='nomor_kamar',
            field=models.CharField(auto_created=True, default='1', max_length=5, primary_key=True, serialize=False),
        ),
    ]
