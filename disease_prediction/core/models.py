from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

# Custom User Model
class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True)
    custom_field = models.CharField(max_length=100, blank=True, null=True)

    # Fix related_name conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True
    )

    def __str__(self):
        return self.username

# Patient Model
class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    #gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])   
    gender = models.CharField(max_length=10, default='Not Specified')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Prediction Model
class Prediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    symptoms = models.TextField(help_text="Symptoms used for prediction, e.g., comma-separated list")
    predicted_disease = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_disease} predicted on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"