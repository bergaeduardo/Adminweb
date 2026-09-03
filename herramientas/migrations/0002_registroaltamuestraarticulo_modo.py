from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herramientas', '0001_registroaltamuestraarticulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='registroaltamuestraarticulo',
            name='modo',
            field=models.CharField(blank=True, choices=[('alta_muestras', 'Alta de muestras'), ('recodificacion', 'Recodificación')], max_length=20, null=True),
        ),
    ]
