# Generated by Django 5.0.1 on 2024-01-13 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_alter_probedata_humidity_alter_probedata_light_level_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='plant',
            name='temperature_min_lte_temperature_max',
        ),
        migrations.RemoveConstraint(
            model_name='plant',
            name='in_sunlight_procent_min_lte_in_sunlight_procent_max',
        ),
        migrations.RemoveConstraint(
            model_name='plant',
            name='humidity_min_lte_humidity_max',
        ),
        migrations.RemoveConstraint(
            model_name='plant',
            name='soil_moisture_min_lte_soil_moisture_max',
        ),
        migrations.AddConstraint(
            model_name='plant',
            constraint=models.CheckConstraint(check=models.Q(('temperature_min__lte', models.F('temperature_max'))), name='temperature_min_lte_temperature_max', violation_error_message='temperature_min must be less than temperature_max'),
        ),
        migrations.AddConstraint(
            model_name='plant',
            constraint=models.CheckConstraint(check=models.Q(('in_sunlight_procent_min__lte', models.F('in_sunlight_procent_max'))), name='in_sunlight_procent_min_lte_in_sunlight_procent_max', violation_error_message='in_sunlight_procent_min must be less than in_sunlight_procent_max'),
        ),
        migrations.AddConstraint(
            model_name='plant',
            constraint=models.CheckConstraint(check=models.Q(('humidity_min__lte', models.F('humidity_max'))), name='humidity_min_lte_humidity_max', violation_error_message='humidity_min must be less than humidity_max'),
        ),
        migrations.AddConstraint(
            model_name='plant',
            constraint=models.CheckConstraint(check=models.Q(('soil_moisture_min__lte', models.F('soil_moisture_max'))), name='soil_moisture_min_lte_soil_moisture_max', violation_error_message='soil_moisture_min must be less than soil_moisture_max'),
        ),
    ]