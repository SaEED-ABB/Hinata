from django.contrib.auth.views import logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required()
def logout(request):
    auth_logout(request)
    return redirect('/')