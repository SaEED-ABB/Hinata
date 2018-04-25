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
        request_body = request.body.decode('utf-8')
        data = json_loads(request_body)

        this_user = request.user
        # this_user = User.objects.get(pk=1)

        username = data['username']
        national_code = data['national_code']
        phone_number = data['phone_number']
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        password = data['password']
    except:
        res_body = {
            "error": "Bad Request"
        }
        return JsonResponse(res_body, status=400)

    
    if User.objects.filter(username=username).exists():
        res_body = {
            "error": "A user with this username is exists."
        }
        return JsonResponse(res_body, status=400)

    if User.objects.filter(email=email).exists():
        res_body = {
            "error": "A user with this email is exists."
        }
        return JsonResponse(res_body, status=400)

    if User.objects.filter(national_code=national_code).exists():
        res_body = {
            "error": "A user with this national code is exists."
        }
        return JsonResponse(res_body, status=400)

    if User.objects.filter(phone_number=phone_number).exists():
        res_body = {
            "error": "A user with this phone number is exists."
        }
        return JsonResponse(res_body, status=400)

    this_user = User()
    this_user.username = username
    this_user.national_code = national_code
    this_user.phone_number = phone_number
    this_user.email = email
    this_user.first_name = first_name
    this_user.last_name = last_name
    this_user.password = make_password(password)
    this_user.account_type = "user"
    this_user.save()
    login(request, authenticate(username=username, password=password))

    res_body = {
        "id": this_user.pk
    }
    return JsonResponse(res_body)
