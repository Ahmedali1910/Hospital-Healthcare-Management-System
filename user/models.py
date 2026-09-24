from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class Role(models.TextChoices):
    ADMIN = 'Admin'
    DOCTOR = 'Doctor'
    PATIENT = 'Patient'

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PATIENT)
    def __str__(self):
        return self.username    