# Generated by Django 3.2.6 on 2023-04-25 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultasTango', '0003_codigoserror_turno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='CodigoProveedor',
            field=models.CharField(max_length=6),
        ),
    ]