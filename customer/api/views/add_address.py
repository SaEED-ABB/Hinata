from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api
from customer.models import UserAddress, User

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def add_address(request):

    user = request.user
    address = request.GET.get('address')
    phone_number = request.GET.get('phone_number')

    if not (address and phone_number):
        res_body = {
            "error": "address or phone_number not provided"
        }
        return JsonResponse(res_body, status=400)

    this_user_address, created = UserAddress.objects.get_or_create(user=user, address=address, phone_number=phone_number)

    if not created:
        res_body = {
            "error": "This address already exists"
        }
        return JsonResponse(res_body, status=400)

    res_body = {
        "success": "Address added for {}".format(user.get_full_name())
    }
    return JsonResponse(res_body)
