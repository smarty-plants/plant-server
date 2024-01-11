from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .serializers import PlantSerializer
from .models import Plant, Probe, ProbeData

import datetime
from .utils import *
import json


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

        dateDayBefore = datetime.datetime.now() - datetime.timedelta(days=1)
        probes = Probe.objects.filter(active=True)
        for x in probes:
            subPayload = {}

            data = ProbeData.objects.filter(read_time__gt = dateDayBefore,probe = x.probe_id)
            plant = x.plant

            subPayload["sunlight_procent"] = getDailyLight(data)
            subPayload["sunlight_min"] = plant.in_sunlight_procent_min
            subPayload["sunlight_max"] = plant.in_sunlight_procent_max
            subPayload["sunlight_readings"] = [y.light_level for y in data]
            
            subPayload["humidity"] = getFirst(data)[0]
            subPayload["humidity_min"] = plant.humidity_min
            subPayload["humidity_max"] = plant.humidity_max
            subPayload["humidity_readings"] = [y.humidity for y in data]

            subPayload["temperature"] = getFirst(data)[1]
            subPayload["temperature_min"] = plant.temperature_min
            subPayload["temperature_max"] = plant.temperature_max
            subPayload["temperature_readings"] = [y.temperature for y in data]

            subPayload["soil_moisture"] = getFirst(data)[2]
            subPayload["soil_moisture_min"] = plant.soil_moisture_min
            subPayload["soil_moisture_max"] = plant.soil_moisture_max
            subPayload["soil_moisture_readings"] = [y.soil_moisture for y in data]

            payload[str(x.probe_id)] = subPayload

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

        
        
        return Response(payload)
