from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.username}"
