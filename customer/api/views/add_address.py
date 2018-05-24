from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api
from customer.models import UserAddress

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def add_address(request):
    """
        add a new address to user addresses
    :param request: user, address, phone_number
    :return: error or success message
    """

    user = request.user
    address = request.POST.get('address')
    phone_number = request.POST.get('phone_number')

    if not (address and phone_number):
        res_body = {
            "error": "address or phone_number not provided"
        }
        return JsonResponse(res_body, status=400)

    res_body, status = user.add_address(address=address, phone_number=phone_number)

    return JsonResponse(res_body, status=status)
