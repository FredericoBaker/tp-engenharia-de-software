
from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("register", views.register, name="register"),
    path("", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile/<str:username>", views.profile, name="profile"),
]
