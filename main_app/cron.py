from django_cron import CronJobBase, Schedule
from django.utils import timezone
from datetime import timedelta
from .models import Medication
from twilio.rest import Client
import os

class MedicationReminderCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'main_app.medication_reminder_cron_job'

    def do(self):
        medications = Medication.objects.all()
        now = timezone.now() - timedelta(hours=3)
        for med in medications:
            if now >= med.next_dose_datetime:
                self.send_reminder(med)
                med.update_next_dose_datetime()

    def send_reminder(self, medication):
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body = (
                    f"🕒 Lembrete de Medicação 🕒\n\n"
                    f"É hora de tomar sua medicação:\n"
                    f"- Medicamento: {medication.name}\n"
                    f"- Dosagem: {medication.dose}\n\n"
                    f"Tomar no horário ajuda no tratamento. 💧 Beba água ao tomar seu remédio.\n"
                    f"Saúde!"
                ),
            from_=f'whatsapp:+{twilio_number}',
            to=f'whatsapp:+55{medication.user.whatsapp_number}'
        )
