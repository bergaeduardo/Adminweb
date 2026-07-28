# Generated manually to fix migration issues

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultasTango', '0015_alter_codigoserror_options_codigoserror_activo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turnoreserva',
            name='orden_compra',
            field=models.CharField(max_length=500, verbose_name='Órdenes de Compra'),
        ),
    ]
