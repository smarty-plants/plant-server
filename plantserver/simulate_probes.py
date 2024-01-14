import os
import random
from time import sleep
from django.utils import timezone


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plantserver.settings")
import django
from tqdm import tqdm

django.setup()

def run_simulation():
    from server.models import Probe, ProbeData
    try:
        while True:
            print(f"Generating data for {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
            probes = Probe.objects.filter(active=True)
            for probe in probes:
                
                last_probe_reading = ProbeData.objects.filter(probe=probe).order_by('-read_time').first()
                if last_probe_reading is None:
                    last_probe_reading = ProbeData.objects.create(
                        probe=probe,
                        temperature=20,
                        humidity=50,
                        soil_moisture=50,
                        light_level=50,
                        read_time=timezone.now(),
                    )
                temperature = last_probe_reading.temperature + random.uniform(-1, 1)
                humidity = last_probe_reading.humidity + random.uniform(-1, 1)
                soil_moisture = last_probe_reading.soil_moisture + random.uniform(-1, 1)
                light_level = last_probe_reading.light_level + random.uniform(-1, 1)
                if temperature > 40:
                    temperature = 40
                if temperature < 0:
                    temperature = 0
                if humidity > 100:
                    humidity = 100
                if humidity < 0:
                    humidity = 0
                if soil_moisture > 100:
                    soil_moisture = 100
                if soil_moisture < 0:
                    soil_moisture = 0
                if light_level > 100:
                    light_level = 100
                if light_level < 0:
                    light_level = 0
                ProbeData.objects.create(
                    probe=probe,
                    temperature=temperature,
                    humidity=humidity,
                    soil_moisture=soil_moisture,
                    light_level=light_level,
                    read_time=timezone.now(),
                )
            sleep(60)
    except KeyboardInterrupt:
        print("Simulation stopped by user")
            
            

if __name__ == "__main__":
    run_simulation()