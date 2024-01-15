from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


class Plant(models.Model):
    class Meta:
        verbose_name = "Plant"
        verbose_name_plural = "Plants"
        constraints = [
            models.CheckConstraint(
                check=models.Q(temperature_min__lte=models.F("temperature_max")),
                name="temperature_min_lte_temperature_max",
                violation_error_message="temperature_min must be less than temperature_max",
            ),
            models.CheckConstraint(
                check=models.Q(
                    in_sunlight_procent_min__lte=models.F("in_sunlight_procent_max")
                ),
                name="in_sunlight_procent_min_lte_in_sunlight_procent_max",
                violation_error_message="in_sunlight_procent_min must be less than in_sunlight_procent_max",
            ),
            models.CheckConstraint(
                check=models.Q(humidity_min__lte=models.F("humidity_max")),
                name="humidity_min_lte_humidity_max",
                violation_error_message="humidity_min must be less than humidity_max",
            ),
            models.CheckConstraint(
                check=models.Q(soil_moisture_min__lte=models.F("soil_moisture_max")),
                name="soil_moisture_min_lte_soil_moisture_max",
                violation_error_message="soil_moisture_min must be less than soil_moisture_max",
            ),
        ]

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
    name = models.CharField(max_length=200, default="Probe")
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProbeData(models.Model):
    class Meta:
        verbose_name = "Probe Data"
        verbose_name_plural = "Probe Data"
    
    probe = models.ForeignKey(Probe, on_delete=models.CASCADE)
    temperature = models.FloatField(
        validators=[MinValueValidator(-100.0), MaxValueValidator(100.0)]
    )
    humidity = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    soil_moisture = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    light_level = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    read_time = models.DateTimeField()

    def __str__(self):
        return f"{self.probe} - {self.read_time}"
