from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herramientas', '0002_registroaltamuestraarticulo_modo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroaltamuestraarticulo',
            name='numero_tarea',
            field=models.TextField(blank=True, null=True),
        ),
    ]
