from json import loads as json_loads

from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api
from customer.models import UserAddress, User

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def add_address(request):
    try:
        request_body = request.body.decode('utf-8')
        data = json_loads(request_body)

        # user = User.objects.get(pk=1)
        user = request.user
        address = data['address']
        phone_number = data['phone_number']
    except:
        res_body = {
            "error": "Bad Request"
        }
        return JsonResponse(res_body, status=400)

    this_user_address, created = UserAddress.objects.get_or_create(user=user, address=address, phone_number=phone_number)

    if not created:
        res_body = {
            "error": "This address is already exists"
        }
        return JsonResponse(res_body, status=400)

    res_body = {
        "id": this_user_address.pk
    }
    return JsonResponse(res_body)
