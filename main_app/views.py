from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render
from django.urls import reverse

from .models import User

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        whatsapp_number = request.POST["whatsapp"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "main_app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, 
                                            email=email, 
                                            password=password, 
                                            whatsapp_number=whatsapp_number)
            user.save()
        except IntegrityError:
            return render(request, "main_app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "main_app/register.html")
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "main_app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "main_app/login.html")

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
