from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render
from django.urls import reverse

from .models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

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
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "main_app/login.html", {"form": form})
    else:
        form = AuthenticationForm()
        return render(request, "main_app/login.html", {"form": form})

def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "main_app/profile.html",{
            "exists": False
        })
    
    return render(request, "main_app/profile.html",{
        "exists": True, 
        "user": user,
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def index(request):
    # If user is not logged in -> Redirects to login page
    if request.user.is_authenticated:
        return render(request, "main_app/index.html", {
            
        })
    else:
        return HttpResponseRedirect(reverse("login"))
