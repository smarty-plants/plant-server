from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .serializers import PlantSerializer
from .models import Plant, Probe, ProbeData


def websocket_view(request):
    return render(request, "websocket_test.html")


class PlantApiView(APIView):
    def get(self, request):
        plants = Plant.objects.all()
        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data)


class ProbeDailyApiView(APIView):
    def get(self, request):
        probes = Probe.objects.filter(active=True)

        #lol
        return Response()
