from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api
from customer.models import UserAddress

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def delete_address(request):
    """
    user can delete each of his addresses
    :param request: user, address_id
    :return: error or success message
    """
    user = request.user
    address_id = request.POST.get('address_id')

    if not address_id:
        res_body = {
            "error": "address_id not provided"
        }
        return JsonResponse(res_body, status=400)

    res_body, status = user.delete_address(address_id=address_id)

    return JsonResponse(res_body, status=status)
