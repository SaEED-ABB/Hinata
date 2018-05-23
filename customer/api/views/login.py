from django.contrib.auth import login as auth_login, authenticate
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, reverse

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='50/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
def login(request):
    """
    to log a user in
    :param request: phone_number, password
    :return: error or success message
    """
    phone_number = request.POST.get('phone_number')
    password = request.POST.get('password')

    if not (phone_number and password):
        res_body = {
            "error": "phone_number or password not provided"
        }
        return JsonResponse(res_body, status=400)
        
    user = authenticate(phone_number=phone_number, password=password)

    if user:
        auth_login(request, user)
        res_body = {
            "success": "User {} successfully logged in".format(user.get_full_name())
        }
        return JsonResponse(res_body, status=201)
    else:
        res_body = {
            'error': 'Username or password is incorrect'
        }
        return JsonResponse(res_body, status=403)
