import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plantserver.settings")
import django
from tqdm import tqdm

django.setup()
from faker import Faker

myfaker = Faker("pl_PL")

def generate_plants():
    from server.models import Plant

    for i in range(3):
        plant = Plant.objects.create(
            name=myfaker.name(),
            plant_species=myfaker.name(),
            temperature_min=myfaker.pyfloat(min_value=0.0, max_value=100.0),
            temperature_max=myfaker.pyfloat(min_value=0.0, max_value=100.0),
            in_sunlight_procent_min=myfaker.pyfloat(min_value=0.0, max_value=100.0),
            in_sunlight_procent_max=myfaker.pyfloat(min_value=0.0, max_value=100.0),
            humidity_min=myfaker.pyfloat(min_value=0.0, max_value=100.0),
            humidity_max=myfaker.pyfloat(min_value=0.0, max_value=100.0),
            soil_moisture_min=myfaker.pyfloat(min_value=0.0, max_value=100.0),
            soil_moisture_max=myfaker.pyfloat(min_value=0.0, max_value=100.0),
        )

def generate_probes():
    from server.models import Probe, Plant

    plants = Plant.objects.all()
    for plant in plants:
        for i in range(3):
            probe = Probe.objects.create(
                name=myfaker.name(),
                plant=plant,
                active=True,
            )
            
def generate_probe_data():
    from server.models import Probe, ProbeData
    from datetime import datetime, timedelta

    probes = Probe.objects.all()
    for probe in tqdm(probes):
        for day in tqdm(range(30)):
            for hour in range(24):
                for minute in range(60):
                    probe_data = ProbeData.objects.create(
                        probe_id=probe.probe_id,
                        temperature=myfaker.pyfloat(min_value=0.0, max_value=100.0),
                        humidity=myfaker.pyfloat(min_value=0.0, max_value=100.0),
                        soil_moisture=myfaker.pyfloat(min_value=0.0, max_value=100.0),
                        light_level=myfaker.pyfloat(min_value=0.0, max_value=100.0),
                        read_time=datetime.now() - timedelta(days=day, hours=hour, minutes=minute),
                    )
        
            

if __name__ == "__main__":
    generate_plants()
    generate_probes()
    generate_probe_data()