# Generated by Django 3.2 on 2025-03-28 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TransporteAPP', '0002_residencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='residencia',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='residencias/'),
        ),
    ]
