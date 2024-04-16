from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from datetime import datetime, timedelta
from django.utils import timezone

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.username}"
    
class Medication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="medications")
    name = models.CharField(max_length=100, verbose_name="Medication Name")
    frequency = models.IntegerField(verbose_name="Frequency of Dosage (Minutes)", help_text="Número de minutos entre doses")
    dose = models.CharField(max_length=100, verbose_name="Dose", help_text="Example: '1 comprimido', '10 mg'")
    start_datetime = models.DateTimeField(verbose_name="Start Date and Time")
    end_date = models.DateField(verbose_name="End Date", help_text="Leave blank if the medication does not have an end date.", blank=True, null=True)
    next_dose_datetime = models.DateTimeField(verbose_name="Next Dose Date and Time", blank=True, null=True)
    observations = models.TextField(verbose_name="Observations", blank=True)

    def __str__(self):
        return f"{self.name} for {self.user.username}"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.next_dose_datetime:
            self.update_next_dose_datetime()
    
    def update_next_dose_datetime(self):
        brazilTime = timezone.now() - timedelta(hours=3)
        startDateTime = self.start_datetime
        if startDateTime:
            timeDeltaSinceStart = brazilTime - startDateTime
            totalMinutesSinceStart = timeDeltaSinceStart.total_seconds() / 60
            minutesSinceLastDose = totalMinutesSinceStart % self.frequency
            minutesToNextDose = self.frequency - minutesSinceLastDose
            nextDoseTime = brazilTime + timedelta(minutes=minutesToNextDose)
            self.next_dose_datetime = nextDoseTime

            self.save()
