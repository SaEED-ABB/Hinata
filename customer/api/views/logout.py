from django.contrib.auth.views import logout as auth_logout
from django.shortcuts import redirect, reverse

from customer.decorators import check_permission_api


@check_permission_api(['user', 'admin'])
def logout(request):
    auth_logout(request)
    return redirect(reverse("frontview:index"))
