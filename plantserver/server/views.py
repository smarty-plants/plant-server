from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .serializers import PlantSerializer
from .models import Plant, Probe, ProbeData

import datetime
from .utils import *
from time import sleep
import uuid


def websocket_view(request):
    return render(request, "websocket_test.html")


class PlantApiView(APIView):
    def get(self, request):
        plants = Plant.objects.all()
        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data)


class ProbeDailyApiView(APIView):
    def get(self, request):
        payload = {}
        payload["read_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        dateDayBefore = datetime.datetime.now() - datetime.timedelta(days=1)
        probes = Probe.objects.all()
        probes_data = []
        for x in probes:
            subPayload = {}

            data = ProbeData.objects.filter(
                read_time__gt=dateDayBefore, probe=x.probe_id
            ).order_by("read_time")
            plant = x.plant

            subPayload["id"] = str(x.probe_id)
            subPayload["name"] = x.name
            subPayload["plant"] = x.plant.name
            subPayload["is_active"] = x.active
            subPayload["plant_species"] = x.plant.plant_species
            subPayload["last_read_time"] = data[0].read_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            subPayload["sunlight_procent"] = getFirst(data)[3]
            subPayload["sunlight_min"] = plant.in_sunlight_procent_min
            subPayload["sunlight_max"] = plant.in_sunlight_procent_max
            subPayload["sunlight_ranges"] = generateRanges(
                plant.in_sunlight_procent_min, plant.in_sunlight_procent_max
            )
            subPayload["humidity"] = getFirst(data)[0]
            subPayload["humidity_min"] = plant.humidity_min
            subPayload["humidity_max"] = plant.humidity_max
            subPayload["humidity_ranges"] = generateRanges(
                plant.humidity_min, plant.humidity_max
            )
            subPayload["temperature"] = getFirst(data)[1]
            subPayload["temperature_min"] = plant.temperature_min
            subPayload["temperature_max"] = plant.temperature_max
            subPayload["temperature_ranges"] = generateRanges(
                plant.temperature_min, plant.temperature_max
            )
            subPayload["soil_moisture"] = getFirst(data)[2]
            subPayload["soil_moisture_min"] = plant.soil_moisture_min
            subPayload["soil_moisture_max"] = plant.soil_moisture_max
            subPayload["soil_moisture_ranges"] = generateRanges(
                plant.soil_moisture_min, plant.soil_moisture_max
            )
            subPayload["data"] = [
                {
                    "time": y.read_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Temperature": y.temperature,
                    "Humidity": y.humidity,
                    "Light level": y.light_level,
                    "Mouisture of soil": y.soil_moisture,
                }
                for y in data
            ]
            probes_data.append(subPayload)

            """print("Sunlight")
            print(getDailyLight(data))
            print(plant.in_sunlight_procent_min)
            print(plant.in_sunlight_procent_max)
            print([y.light_level for y in data])
            print("Hum")
            print(getFirst(data)[0])
            print(plant.humidity_min)
            print(plant.humidity_max)
            print([y.humidity for y in data])
            print("temp")
            print(getFirst(data)[1])
            print(plant.temperature_min)
            print(plant.temperature_max)
            print([y.temperature for y in data])
            print("soil")
            print(getFirst(data)[2])
            print(plant.soil_moisture_min)
            print(plant.soil_moisture_max)
            print([y.soil_moisture for y in data])"""
        payload["data"] = probes_data

        return Response(payload)

class ProbeCurrentReadingsApiView(APIView):
    def get(self, request):
        payload = {}
        payload["read_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        dateDayBefore = datetime.datetime.now() - datetime.timedelta(days=1)
        probes = Probe.objects.all()
        probes_data = []
        for x in probes:
            subPayload = {}

            data = ProbeData.objects.filter(
                read_time__gt=dateDayBefore, probe=x.probe_id
            ).order_by("read_time")
            plant = x.plant

            subPayload["id"] = str(x.probe_id)
            subPayload["name"] = x.name
            subPayload["plant"] = x.plant.name
            subPayload["is_active"] = x.active
            subPayload["plant_species"] = x.plant.plant_species
            subPayload["last_read_time"] = data[0].read_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            last_reading = getFirst(data)
            subPayload["sunlight_procent"] = last_reading[3]
            subPayload["sunlight_status"] = getValueStatus(last_reading[3], plant.in_sunlight_procent_min, plant.in_sunlight_procent_max)
            subPayload["humidity"] = last_reading[0]
            subPayload["humidity_status"] = getValueStatus(last_reading[0], plant.humidity_min, plant.humidity_max)
            subPayload["temperature"] = last_reading[1]
            subPayload["temperature_status"] = getValueStatus(last_reading[1], plant.temperature_min, plant.temperature_max)
            subPayload["soil_moisture"] = last_reading[2]
            subPayload["soil_moisture_status"] = getValueStatus(last_reading[2], plant.soil_moisture_min, plant.soil_moisture_max)
            probes_data.append(subPayload)
        payload["data"] = probes_data

        return Response(payload)
    

class ProbeDetailApiView(APIView):
    def get(self, request, probe_id):
        payload = {}
        payload["read_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        dateDayBefore = datetime.datetime.now() - datetime.timedelta(days=1)
        probe = Probe.objects.get(probe_id=probe_id)
        subPayload = {}

        data = ProbeData.objects.filter(
            read_time__gt=dateDayBefore, probe=probe_id
        ).order_by("read_time")
        plant = probe.plant

        subPayload["id"] = str(probe.probe_id)
        subPayload["name"] = probe.name
        subPayload["plant"] = probe.plant.name
        subPayload["is_active"] = probe.active
        subPayload["plant_species"] = probe.plant.plant_species
        subPayload["last_read_time"] = data[0].read_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        subPayload["sunlight_procent"] = getFirst(data)[3]
        subPayload["sunlight_min"] = plant.in_sunlight_procent_min
        subPayload["sunlight_max"] = plant.in_sunlight_procent_max
        subPayload["sunlight_ranges"] = generateRanges(
            plant.in_sunlight_procent_min, plant.in_sunlight_procent_max
        )
        subPayload["humidity"] = getFirst(data)[0]
        subPayload["humidity_min"] = plant.humidity_min
        subPayload["humidity_max"] = plant.humidity_max
        subPayload["humidity_ranges"] = generateRanges(
            plant.humidity_min, plant.humidity_max
        )
        subPayload["temperature"] = getFirst(data)[1]
        subPayload["temperature_min"] = plant.temperature_min
        subPayload["temperature_max"] = plant.temperature_max
        subPayload["temperature_ranges"] = generateRanges(
            plant.temperature_min, plant.temperature_max
        )
        subPayload["soil_moisture"] = getFirst(data)[2]
        subPayload["soil_moisture_min"] = plant.soil_moisture_min
        subPayload["soil_moisture_max"] = plant.soil_moisture_max
        subPayload["soil_moisture_ranges"] = generateRanges(
            plant.soil_moisture_min, plant.soil_moisture_max
        )
        subPayload["data"] = [
                {
                    "id": y.pk,
                    "time": y.read_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Temperature": y.temperature,
                    "Humidity": y.humidity,
                    "Light level": y.light_level,
                    "Mouisture of soil": y.soil_moisture,
                }
                for y in data
            ]
        payload["data"] = subPayload
        
        return Response(payload)
    

class ProbeCreateView(APIView):
    def post(self,request):
        data = request.data
        probe_name = data.get('probe_name',None)
        plant_id = data.get('plant_id',None)

        if(probe_name is None or plant_id is None):
            return Response(
                    {"status": "failed", "message": f"Bad/Uncomplete request"}
                    ,status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            uuid_obj = uuid.UUID(plant_id)
        except Exception as e:
            return Response(
                    {"status": "failed", "message": f"Wrong plant UUID"}
                    ,status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )

        plant = Plant.objects.get(plant_id=plant_id)

        if(plant is None):
            return Response(
                    {"status": "failed", "message": f"Plant not found"}
                    ,status=status.HTTP_409_CONFLICT
                )
        
        try:
            probe_created = Probe(
                    name=probe_name,
                    plant=plant,
                    active=True,
                )
            
            probe_created.full_clean()
        except Exception as e:
            return Response(
                    {"status": "failed", "message": f"Error occurred during probe creation"}
                    ,status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        else:
            probe_created.save()
            return Response(
                        {"status": "success","probe_id":str(probe_created.probe_id),"message": f"Successfully create probe {probe_name}"}
                        ,status=status.HTTP_201_CREATED
                    )
        

class PlantCreateView(APIView):
    def post(self,request):
        data = request.data
        
        dict = {
            'name': data.get('name',None),
            'plant_species': data.get('plant_species',None),
            'temperature_min':data.get('temperature_min',None),
            'temperature_max':data.get('temperature_max',None),
            'in_sunlight_procent_min':data.get('in_sunlight_procent_min',None),
            'in_sunlight_procent_max':data.get('in_sunlight_procent_max',None),
            'humidity_min':data.get('humidity_min',None),
            'humidity_max':data.get('humidity_max',None),
            'soil_moisture_min':data.get('soil_moisture_min',None),
            'soil_moisture_max':data.get('soil_moisture_max',None),
        }

        for x in dict:
            if(dict[x] is None):
                return Response(
                    {"status": "failed", "message": f"Bad/Uncomplete request"}
                    ,status=status.HTTP_400_BAD_REQUEST
                )
            
        try:
            plant_created = Plant(
                    name=dict['name'],
                    plant_species=dict['plant_species'],
                    temperature_min=dict['temperature_min'],
                    temperature_max=dict['temperature_max'],
                    in_sunlight_procent_min=dict['in_sunlight_procent_min'],
                    in_sunlight_procent_max=dict['in_sunlight_procent_max'],
                    humidity_min=dict['humidity_min'],
                    humidity_max=dict['humidity_max'],
                    soil_moisture_min=dict['soil_moisture_min'],
                    soil_moisture_max=dict['soil_moisture_max'],
                )
            
            plant_created.full_clean()
        except Exception as e:
            return Response(
                    {"status": "failed", "message": f"Error occurred during plant creation"}
                    ,status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        else:
            plant_created.save()
            return Response(
                        {"status": "success","plant_id":str(plant_created.plant_id),"message": f"Successfully create plant {dict['name']}"}
                        ,status=status.HTTP_201_CREATED
                    )

        