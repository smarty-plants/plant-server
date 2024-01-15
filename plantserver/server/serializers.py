from rest_framework import serializers
from .models import Plant, Probe

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = "__all__"


class ProbeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probe
        fields = "__all__"