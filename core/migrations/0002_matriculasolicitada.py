# Generated by Django 2.1 on 2018-12-11 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatriculaSolicitada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricula', models.CharField(max_length=7, verbose_name='Matrícula')),
                ('fecha_solicitada', models.DateTimeField(verbose_name='Fecha Solicitud')),
                ('motivo', models.CharField(max_length=50, verbose_name='Motivo')),
                ('activo', models.BooleanField(verbose_name='Activo')),
            ],
            options={
                'ordering': ['-fecha_solicitada'],
            },
        ),
    ]
