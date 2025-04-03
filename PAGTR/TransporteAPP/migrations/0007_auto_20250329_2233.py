# Generated by Django 3.2 on 2025-03-30 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TransporteAPP', '0006_ruta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ruta',
            old_name='descripcion',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='ruta',
            old_name='titulo',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='ruta',
            name='tipo_vehiculo',
        ),
        migrations.AddField(
            model_name='ruta',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ruta',
            name='vehiculo',
            field=models.CharField(choices=[('Carro', 'Carro'), ('Moto', 'Moto')], default=3, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ruta',
            name='cupos',
            field=models.IntegerField(default=1),
        ),
    ]
