from json import loads as json_loads

from django.contrib.auth import login as auth_login, authenticate
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, reverse

from ratelimit.decorators import ratelimit

from customer.models import User


@ratelimit(key='ip', rate='50/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
def login(request):
    try:
        # request_body = request.body.decode('utf-8')
        # data = json_loads(request_body)
        # username = data['username']
        # password = data['password']
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        print(phone_number, password)
    except:
        res_body = {
            "error": "Bad Request"
        }
        return JsonResponse(res_body, status=400)
        
    user = authenticate(phone_number=phone_number, password=password)
    print(user)
    if user:
        auth_login(request, user)
        return redirect(reverse("frontview:index"))
    else:
        res_body = {
            'message': 'Please check your username and password'
        }
        return JsonResponse(res_body, status=403)
