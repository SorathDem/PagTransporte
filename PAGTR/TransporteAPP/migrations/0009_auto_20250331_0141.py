# Generated by Django 3.2 on 2025-03-31 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TransporteAPP', '0008_cupopordia'),
    ]

    operations = [
        migrations.AddField(
            model_name='cupopordia',
            name='cupos_dia',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cupopordia',
            name='dia',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='cupopordia',
            name='ruta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cupos_dia', to='TransporteAPP.ruta'),
        ),
    ]
