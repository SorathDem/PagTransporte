# Generated by Django 3.2 on 2025-03-28 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TransporteAPP', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Residencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('ubicacion', models.URLField()),
            ],
        ),
    ]
