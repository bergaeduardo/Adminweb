# Generated by Django 3.2.6 on 2024-05-12 23:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultasTango', '0006_eb_facturamanual'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eb_facturamanual',
            old_name='imgFact_A',
            new_name='imgFacturo',
        ),
        migrations.RenameField(
            model_name='eb_facturamanual',
            old_name='numeroFact_A',
            new_name='numeroFactura',
        ),
    ]
