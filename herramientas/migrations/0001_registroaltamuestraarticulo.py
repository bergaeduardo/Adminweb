from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroAltaMuestraArticulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('accion', models.CharField(choices=[('importar', 'Importar datos'), ('ejecutar', 'Ejecutar recodificación')], max_length=20)),
                ('filas', models.JSONField()),
                ('numero_tarea', models.CharField(blank=True, max_length=100, null=True)),
                ('filas_con_error', models.JSONField(blank=True, null=True)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Registro de alta de muestra de artículo',
                'verbose_name_plural': 'Registros de altas de muestras de artículos',
                'ordering': ['-fecha'],
            },
        ),
    ]
