from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    patient_name = models.CharField(max_length=100)
    symptoms = models.TextField()
    disease = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.disease}"