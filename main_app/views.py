from django.contrib.auth import login, logout
from django.db import models
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Medication
from .forms import CustomUserCreationForm
from .forms import CustomAuthenticationForm
from datetime import datetime, timedelta
from django.utils import timezone


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
        for med in userMeds:
            med.update_next_dose_datetime()

        userMedsForToday = [med for med in userMeds if med.next_dose_datetime.date() == brazilTime.date()]

        return render(request, "main_app/index.html", {
            'userMedsForToday': userMedsForToday
        })
    else:
        return HttpResponseRedirect(reverse("login"))
