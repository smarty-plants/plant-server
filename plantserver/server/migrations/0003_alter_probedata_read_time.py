# Generated by Django 5.0.1 on 2024-01-11 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_alter_probedata_options_alter_plant_plant_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='probedata',
            name='read_time',
            field=models.DateTimeField(),
        ),
    ]
