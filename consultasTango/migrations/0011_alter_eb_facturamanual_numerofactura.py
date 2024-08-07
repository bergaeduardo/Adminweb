# Generated by Django 3.2.6 on 2024-07-01 17:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultasTango', '0010_alter_eb_facturamanual_numerofactura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eb_facturamanual',
            name='numeroFactura',
            field=models.CharField(max_length=14, validators=[django.core.validators.RegexValidator(message='El formato debe ser XXXXX-XXXXXXX', regex='^\\d{5}-\\d{8}$')]),
        ),
    ]
