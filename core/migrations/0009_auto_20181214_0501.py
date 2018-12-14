# Generated by Django 2.1 on 2018-12-14 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20181213_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patrullero',
            name='activo',
            field=models.BooleanField(default=False, verbose_name='Activo'),
        ),
        migrations.AlterField(
            model_name='patrullero',
            name='cedula',
            field=models.CharField(max_length=10, unique=True, verbose_name='Cédula'),
        ),
    ]
