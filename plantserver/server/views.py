from django.shortcuts import get_object_or_404, render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .serializers import PlantSerializer, ProbeSerializer
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
            subPayload["is_active"] = x.active
            if plant is None:
                subPayload.update(getDataForEmptyPlant())
            else:
                subPayload["plant"] = x.plant.name
                subPayload["plant_species"] = x.plant.plant_species
                if len(data) == 0:
                    subPayload["last_read_time"] = None
                else:
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
            subPayload["is_active"] = x.active
            if plant is None:
                subPayload.update(getDataForEmptyPlant())
            else:
                subPayload["plant"] = x.plant.name
                subPayload["plant_species"] = x.plant.plant_species
                if len(data) == 0:
                    subPayload["last_read_time"] = None
                else:
                    subPayload["last_read_time"] = data[0].read_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                last_reading = getFirst(data)
                subPayload["sunlight_procent"] = last_reading[3]
                subPayload["sunlight_status"] = getValueStatus(
                    last_reading[3],
                    plant.in_sunlight_procent_min,
                    plant.in_sunlight_procent_max,
                )
                subPayload["humidity"] = last_reading[0]
                subPayload["humidity_status"] = getValueStatus(
                    last_reading[0], plant.humidity_min, plant.humidity_max
                )
                subPayload["temperature"] = last_reading[1]
                subPayload["temperature_status"] = getValueStatus(
                    last_reading[1], plant.temperature_min, plant.temperature_max
                )
                subPayload["soil_moisture"] = last_reading[2]
                subPayload["soil_moisture_status"] = getValueStatus(
                    last_reading[2], plant.soil_moisture_min, plant.soil_moisture_max
                )
            probes_data.append(subPayload)
        payload["data"] = probes_data

        return Response(payload)


class ProbeDetailApiView(APIView):
    def get(self, request, probe_id):
        payload = {}
        payload["read_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        probe = Probe.objects.get(probe_id=probe_id)
        subPayload = {}

        data = ProbeData.objects.filter(probe=probe).order_by("read_time")
        plant = probe.plant

        subPayload["id"] = str(probe.probe_id)
        subPayload["name"] = probe.name
        subPayload["is_active"] = probe.active
        if plant is None:
            subPayload.update(getDataForEmptyPlant())
        else:
            subPayload["plant"] = probe.plant.name
            subPayload["plant_species"] = probe.plant.plant_species
            if len(data) == 0:
                subPayload["last_read_time"] = None
            else:
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
    def post(self, request):
        serializer = ProbeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PlantCreateView(APIView):
    def post(self, request):
        serializer = PlantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CheckProbeApi(APIView):
    def post(self, request):
        uuid = request.data.get("uuid")
        if uuid is None:
            return Response(
                {"status": "failed", "message": f"Bad/Uncomplete request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            if Probe.objects.filter(probe_id=uuid).exists():
                return Response(
                    {"status": "success", "message": f"UUID is correct"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "failed", "message": f"UUID is incorrect"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except:
            return Response(
                {"status": "failed", "message": f"UUID is incorrect"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CreateProbeApi(APIView):
    def post(self, request):
        probe = Probe.objects.create()
        return Response({"probe_id": str(probe.probe_id)})


class ProbeDetailApi(APIView):
    def get(self, request, probe_id):
        probe = get_object_or_404(Probe, probe_id=probe_id)
        serializer = ProbeSerializer(probe)
        return Response(serializer.data)

    def put(self, request, probe_id):
        probe = get_object_or_404(Probe, probe_id=probe_id)
        serializer = ProbeSerializer(probe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
