# Generated by Django 3.2.6 on 2024-07-26 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultasTango', '0011_alter_eb_facturamanual_numerofactura'),
    ]

    operations = [
        migrations.AddField(
            model_name='eb_facturamanual',
            name='fechaVencimiento',
            field=models.DateField(blank=True, null=True),
        ),
    ]