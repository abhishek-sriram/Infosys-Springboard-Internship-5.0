from django.db import models

# Create your models here.

class StressInput(models.Model):
    snoring_rate = models.FloatField()
    respiratory_rate = models.FloatField()
    body_temperature = models.FloatField()
    limb_movement = models.FloatField()
    blood_oxygen = models.FloatField()
    eye_movements = models.FloatField()
    sleep_hours = models.FloatField()
    heart_rate = models.FloatField()

class StressPrediction(models.Model):
    input_data = models.ForeignKey(StressInput, on_delete=models.CASCADE)
    predicted_stress_level = models.FloatField()


