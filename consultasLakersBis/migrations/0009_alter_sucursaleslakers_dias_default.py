from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Actualiza los campos de dias (lunes-domingo) para reflejar que la columna
    en SQL Server es NOT NULL con default False. Solo actualiza el estado de
    migracion, sin cambiar el esquema ya que la DB ya tiene los constraint correctos.
    """

    dependencies = [
        ('consultasLakersBis', '0008_add_missing_sucursaleslakers_fields'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AlterField(
                    model_name='sucursaleslakers',
                    name='lunes',
                    field=models.BooleanField(blank=True, db_column='LUNES', default=False),
                ),
                migrations.AlterField(
                    model_name='sucursaleslakers',
                    name='martes',
                    field=models.BooleanField(blank=True, db_column='MARTES', default=False),
                ),
                migrations.AlterField(
                    model_name='sucursaleslakers',
                    name='miercoles',
                    field=models.BooleanField(blank=True, db_column='MIERCOLES', default=False),
                ),
                migrations.AlterField(
                    model_name='sucursaleslakers',
                    name='jueves',
                    field=models.BooleanField(blank=True, db_column='JUEVES', default=False),
                ),
                migrations.AlterField(
                    model_name='sucursaleslakers',
                    name='viernes',
                    field=models.BooleanField(blank=True, db_column='VIERNES', default=False),
                ),
                migrations.AlterField(
                    model_name='sucursaleslakers',
                    name='sabado',
                    field=models.BooleanField(blank=True, db_column='SABADO', default=False),
                ),
                migrations.AlterField(
                    model_name='sucursaleslakers',
                    name='domingo',
                    field=models.BooleanField(blank=True, db_column='DOMINGO', default=False),
                ),
            ],
        ),
    ]
