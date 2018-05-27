from django.contrib.auth.views import logout as auth_logout
from django.shortcuts import redirect, reverse

from customer.decorators import check_authentication_status


@check_authentication_status()
def logout(request):
    """
    log a user out
    :param request: request itself!
    :return: redirect to index page
    """
    auth_logout(request)
    return redirect(reverse("frontview:index"))
