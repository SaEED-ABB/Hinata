from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.utils import timezone


def logout(request):
    auth_logout(request)
    return redirect("/")