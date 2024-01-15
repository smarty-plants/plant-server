import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plantserver.settings")
import django
from tqdm import tqdm
from django.utils import timezone

django.setup()
from faker import Faker

myfaker = Faker("pl_PL")

def generate_plants():
    from server.models import Plant
    flowers = [
        "Amarylis",
        "Anturium",
        "Astry",
    ]
    
    for flower in flowers:
        Plant.objects.create(
            name=flower,
            plant_species=flower + " sp.",
            temperature_min=myfaker.pyfloat(min_value=0.0, max_value=50.0),
            temperature_max=myfaker.pyfloat(min_value=50.0, max_value=100.0),
            in_sunlight_procent_min=myfaker.pyfloat(min_value=0.0, max_value=50.0),
            in_sunlight_procent_max=myfaker.pyfloat(min_value=50.0, max_value=100.0),
            humidity_min=myfaker.pyfloat(min_value=0.0, max_value=50.0),
            humidity_max=myfaker.pyfloat(min_value=50.0, max_value=100.0),
            soil_moisture_min=myfaker.pyfloat(min_value=0.0, max_value=50.0),
            soil_moisture_max=myfaker.pyfloat(min_value=50.0, max_value=100.0),
        )

def generate_probes():
    from server.models import Probe, Plant

    plants = Plant.objects.all()
    for index, plant in enumerate(plants):
            Probe.objects.create(
                name="Probe " + str(index+1),
                plant=plant,
                active=True,
            )
            
def generate_probe_data(for_how_many_days=3):
    from server.models import Probe, ProbeData
    from datetime import datetime, timedelta

    probes = Probe.objects.all()
    for probe in tqdm(probes):
        last_temperature = myfaker.pyfloat(min_value=20, max_value=35)
        last_humidity = myfaker.pyfloat(min_value=0.0, max_value=100.0)
        last_soil_moisture = myfaker.pyfloat(min_value=0.0, max_value=100.0)
        last_light_level = myfaker.pyfloat(min_value=0.0, max_value=100.0)
        for day in tqdm(range(for_how_many_days)):
            for hour in tqdm(range(24)):
                for minute in range(30):
                    ProbeData.objects.create(
                        probe_id=probe.probe_id,
                        temperature=last_temperature,
                        humidity=last_humidity,
                        soil_moisture=last_soil_moisture,
                        light_level=last_light_level,
                        read_time=timezone.now() - timedelta(days=day, hours=hour, minutes=minute*2),
                    )
                    last_temperature += random.uniform(-0.5, 0.5)
                    last_humidity += random.uniform(-0.5, 0.5)
                    last_soil_moisture += random.uniform(-0.5, 0.5)
                    last_light_level += random.uniform(-0.5, 0.5)
                    if last_temperature > 35:
                        last_temperature = 35
                    if last_temperature < 20:
                        last_temperature = 20
                    if last_humidity > 100:
                        last_humidity = 100
                    if last_humidity < 0:
                        last_humidity = 0
                    if last_soil_moisture > 100:
                        last_soil_moisture = 100
                    if last_soil_moisture < 0:
                        last_soil_moisture = 0
                    if last_light_level > 100:
                        last_light_level = 100
                    if last_light_level < 0:
                        last_light_level = 0
            

if __name__ == "__main__":

    generate_plants()
    generate_probes()
    generate_probe_data()