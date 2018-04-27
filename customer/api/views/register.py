from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login

from customer.forms import UserCreationForm
from customer.models import User

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
def register(request):

    phone_number = request.GET.get('phone_number')
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    password = request.GET.get('password1')
    password_confirm = request.GET.get('password2')

    if not (phone_number and first_name and last_name and password and password_confirm):
        res_body = {
            "error": "phone_number or first_name or last_name or password or password_confirm not provided"
        }
        return JsonResponse(res_body, status=400)

    if User.objects.filter(phone_number=phone_number).exists():
        res_body = {
            "error": "A user with this phone_number does exist"
        }
        return JsonResponse(res_body, status=400)

    form = UserCreationForm(data={
        "phone_number": phone_number,
        "first_name": first_name,
        "last_name": last_name,
        "password1": password,
        "password2": password_confirm
    })
    if form.is_valid():
        new_user = form.save()
        login(request, new_user)

        res_body = {
            "success": "User {} successfully registered.".format(new_user.get_full_name())
        }
        return JsonResponse(res_body)
    else:
        res_body = {
            'error': 'provided form is invalid'
        }
        return JsonResponse(res_body, status=400)
