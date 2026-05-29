from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultasLakersBis', '0007_alter_sucursaleslakers_retiro_expres'),
    ]

    operations = [
        # Sincroniza el estado de migracion para llave_prueba (db_column cambio de LLAVE_PRUEBA a NRO_SUC_ACTUAL)
        # No ejecuta SQL ya que la columna fue renombrada manualmente en la DB
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AlterField(
                    model_name='sucursaleslakers',
                    name='llave_prueba',
                    field=models.BinaryField(blank=True, db_column='NRO_SUC_ACTUAL', null=True),
                ),
            ],
        ),

        # Agrega los campos de dias y mail_grupo_emp usando SQL condicional para evitar
        # fallo si las columnas ya existen en la DB
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
IF COL_LENGTH('SUCURSALES_LAKERS', 'LUNES') IS NULL
    ALTER TABLE SUCURSALES_LAKERS ADD LUNES BIT NULL;
IF COL_LENGTH('SUCURSALES_LAKERS', 'MARTES') IS NULL
    ALTER TABLE SUCURSALES_LAKERS ADD MARTES BIT NULL;
IF COL_LENGTH('SUCURSALES_LAKERS', 'MIERCOLES') IS NULL
    ALTER TABLE SUCURSALES_LAKERS ADD MIERCOLES BIT NULL;
IF COL_LENGTH('SUCURSALES_LAKERS', 'JUEVES') IS NULL
    ALTER TABLE SUCURSALES_LAKERS ADD JUEVES BIT NULL;
IF COL_LENGTH('SUCURSALES_LAKERS', 'VIERNES') IS NULL
    ALTER TABLE SUCURSALES_LAKERS ADD VIERNES BIT NULL;
IF COL_LENGTH('SUCURSALES_LAKERS', 'SABADO') IS NULL
    ALTER TABLE SUCURSALES_LAKERS ADD SABADO BIT NULL;
IF COL_LENGTH('SUCURSALES_LAKERS', 'DOMINGO') IS NULL
    ALTER TABLE SUCURSALES_LAKERS ADD DOMINGO BIT NULL;
IF COL_LENGTH('SUCURSALES_LAKERS', 'MAIL_GRUP_EMP') IS NULL
    ALTER TABLE SUCURSALES_LAKERS ADD MAIL_GRUP_EMP NVARCHAR(200) NULL;
                    """,
                    reverse_sql=migrations.RunSQL.noop,
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='sucursaleslakers',
                    name='lunes',
                    field=models.BooleanField(db_column='LUNES', default=False),
                ),
                migrations.AddField(
                    model_name='sucursaleslakers',
                    name='martes',
                    field=models.BooleanField(db_column='MARTES', default=False),
                ),
                migrations.AddField(
                    model_name='sucursaleslakers',
                    name='miercoles',
                    field=models.BooleanField(db_column='MIERCOLES', default=False),
                ),
                migrations.AddField(
                    model_name='sucursaleslakers',
                    name='jueves',
                    field=models.BooleanField(db_column='JUEVES', default=False),
                ),
                migrations.AddField(
                    model_name='sucursaleslakers',
                    name='viernes',
                    field=models.BooleanField(db_column='VIERNES', default=False),
                ),
                migrations.AddField(
                    model_name='sucursaleslakers',
                    name='sabado',
                    field=models.BooleanField(db_column='SABADO', default=False),
                ),
                migrations.AddField(
                    model_name='sucursaleslakers',
                    name='domingo',
                    field=models.BooleanField(db_column='DOMINGO', default=False),
                ),
                migrations.AddField(
                    model_name='sucursaleslakers',
                    name='mail_grupo_emp',
                    field=models.CharField(blank=True, db_column='MAIL_GRUP_EMP', max_length=200, null=True),
                ),
            ],
        ),
    ]
