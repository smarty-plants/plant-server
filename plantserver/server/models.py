from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


class Plant(models.Model):
    class Meta:
        verbose_name = "Plant"
        verbose_name_plural = "Plants"

    plant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    plant_species = models.CharField(max_length=200)

    temperature_min = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    temperature_max = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    in_sunlight_procent_min = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    in_sunlight_procent_max = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    humidity_min = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    humidity_max = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    soil_moisture_min = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    soil_moisture_max = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    def __str__(self):
        return self.name


class Probe(models.Model):
    probe_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProbeData(models.Model):
    class Meta:
        verbose_name = "Probe Data"
        verbose_name_plural = "Probe Data"
    
    probe = models.ForeignKey(Probe, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    soil_moisture = models.FloatField()
    light_level = models.FloatField()
    read_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.probe} - {self.read_time}"
