# Generated by Django 5.0.1 on 2024-01-15 19:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_remove_plant_temperature_min_lte_temperature_max_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='probe',
            name='plant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='server.plant'),
        ),
    ]
