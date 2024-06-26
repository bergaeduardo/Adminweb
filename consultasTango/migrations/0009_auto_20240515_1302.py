# Generated by Django 3.2.6 on 2024-05-15 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultasTango', '0008_rename_imgfacturo_eb_facturamanual_imgfactura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eb_facturamanual',
            name='fechaRegistro',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='eb_facturamanual',
            name='imgFactura',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='eb_facturamanual',
            name='tipoFactura',
            field=models.IntegerField(choices=[(0, 'Factura-A'), (1, 'Factura-B')]),
        ),
    ]
