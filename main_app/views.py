import os
from dotenv import load_dotenv

from django.contrib.auth import login, logout
from django.db import models
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Medication
from .forms import CustomUserCreationForm
from .forms import CustomAuthenticationForm
from .forms import CustomMedicationCreationForm
from datetime import datetime, timedelta
from django.utils import timezone

from twilio.rest import Client
from textwrap import dedent

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "main_app/register.html", {
                "form": form
            })
    else:
        form = CustomUserCreationForm()
        return render(request, "main_app/register.html", {"form": form})
    
def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "main_app/login.html", {"form": form})
    else:
        form = CustomAuthenticationForm()
        return render(request, "main_app/login.html", {"form": form})

def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "main_app/profile.html",{
            "exists": False
        })
    
    if request.user.username == username:
        return render(request, "main_app/profile.html",{
            "exists": True, 
            "user": user,
        })
    else:
        return logout_view(request)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def index(request):
    # If user is not logged in -> Redirects to login page
    if request.user.is_authenticated:
        brazilTime = timezone.now() - timedelta(hours=3)
        userMeds = request.user.medications.filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gt=brazilTime)
        )

        userMedsForToday = [med for med in userMeds if med.next_dose_datetime.date() == brazilTime.date()]
        
        return render(request, "main_app/index.html", {
            'userMedsForToday': userMedsForToday,
            'userMeds': userMeds
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def send_whatsapp_message(phone, content):
    message = client.messages.create(
        from_=f'whatsapp:+{TWILIO_NUMBER}',
        body=content,
        to=f'whatsapp:+55{phone}',
    )

def build_message(user, form_instance):
    proxima_dose = form_instance.start_datetime + timedelta(hours=form_instance.frequency)
    message = (
        f"*Nova medicação adicionada!* 📝\n\n"
        f"Olá, *{user.username}*!\n\n"
        "🙌 Sua medicação foi cadastrada com sucesso no sistema. Aqui estão os detalhes:\n\n"
        f"- *Medicamento*: {form_instance.name}\n"
        f"- *Dosagem*: {form_instance.dose}\n"
        f"- *Frequência*: A cada {form_instance.frequency} minutos\n"
        f"- *Começa em*: {form_instance.start_datetime.strftime('%d/%m/%Y às %H:%M')}\n"
        f"- *Próxima dose*: {proxima_dose.strftime('%d/%m/%Y às %H:%M')}\n\n"
        "🔔 Você receberá lembretes automáticos para tomar seu medicamento conforme programado.\n\n"
        "Desejamos a você saúde e bem-estar! 💊✨"
    )

    return message

def register_medication(request):
    if request.method == "POST":
        form = CustomMedicationCreationForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            message = build_message(request.user, form.instance)
            send_whatsapp_message(phone=request.user.whatsapp_number, content=message)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "main_app/registerMedication.html", {"form": form})
    else:
        form = CustomMedicationCreationForm()
        return render(request, "main_app/registerMedication.html", {"form": form})
