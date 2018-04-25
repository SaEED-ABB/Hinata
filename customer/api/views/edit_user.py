from json import loads as json_loads

from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist

from customer.decorators import check_permission_api
from customer.models import User

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def edit_user(request):
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
    except:
        res_body = {
            "error": "Bad Request"
        }
        return JsonResponse(res_body, status=400)

    this_user.username = username
    this_user.national_code = national_code
    this_user.phone_number = phone_number
    this_user.email = email
    this_user.first_name = first_name
    this_user.last_name = last_name
    this_user.save()
    return JsonResponse({})
