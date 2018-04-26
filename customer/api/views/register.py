from json import loads as json_loads

from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login

from customer.decorators import check_permission_api
from customer.models import User

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
def register(request):
    try:
        username = request.GET.get('username')
        # national_code = data['national_code']
        phone_number = request.GET.get('phone_number')
        email = request.GET.get('email')
        first_name = request.GET.get('first_name', '')
        last_name = request.GET.get('last_name', '')
        password = request.GET.get('password')
    except:
        res_body = {
            "error": "Bad Request"
        }
        return JsonResponse(res_body, status=400)
    
    if User.objects.filter(username=username).exists():
        res_body = {
            "error": "A user with this username exists."
        }
        return JsonResponse(res_body, status=400)

    if User.objects.filter(email=email).exists():
        res_body = {
            "error": "A user with this email exists."
        }
        return JsonResponse(res_body, status=400)

    if User.objects.filter(phone_number=phone_number).exists():
        res_body = {
            "error": "A user with this phone number exists."
        }
        return JsonResponse(res_body, status=400)

    new_user = User.objects.create(
        username=username,
        phone_number=phone_number,
        email=email,
        first_name=first_name,
        last_name=last_name,
        account_type='user'
    )

    new_user.set_password(password)
    new_user.save()

    login(request, authenticate(username=username, password=password))

    res_body = {
        "id": new_user.pk
    }
    return JsonResponse(res_body)
