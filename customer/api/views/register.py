from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login

from customer.forms import UserCreationForm
from customer.models import User

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
def register(request):
    try:
        phone_number = request.POST.get('phone_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password1')
        password_confirm = request.POST.get('password2')
    except:
        res_body = {
            "error": "Bad Request"
        }
        return JsonResponse(res_body, status=400)

    if User.objects.filter(phone_number=phone_number).exists():
        res_body = {
            "error": "A user with this phone number exists."
        }
        return JsonResponse(res_body, status=400)
    print(request.POST)
    form = UserCreationForm(data=request.POST)
    if form.is_valid():
        new_user = form.save()
        # new_user.set_password(password)
        # new_user.save()

        login(request, new_user)

        res_body = {
            "id": new_user.pk
        }
        return JsonResponse(res_body)
    else:
        return JsonResponse({'message': 'invalid form'})

    # new_user = User.objects.create(
    #     phone_number=phone_number,
    #     first_name=first_name,
    #     last_name=last_name,
    # )
    # new_user.set_password(password)
    # new_user.save()


