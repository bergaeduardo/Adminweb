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
            name='RegistroTransferenciaDeposito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('accion', models.CharField(choices=[('validar', 'Validar lote'), ('ejecutar', 'Ejecutar transferencia')], max_length=20)),
                ('lote_id', models.UUIDField(db_index=True)),
                ('filas', models.JSONField()),
                ('filas_con_error', models.JSONField(blank=True, null=True)),
                ('numero_tarea', models.TextField(blank=True, null=True)),
                ('nro_comprobante', models.TextField(blank=True, null=True)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Registro de transferencia entre depósitos',
                'verbose_name_plural': 'Registros de transferencias entre depósitos',
                'ordering': ['-fecha'],
            },
        ),
    ]
