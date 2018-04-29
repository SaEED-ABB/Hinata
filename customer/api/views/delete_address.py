from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def delete_address(request):

    user = request.user
    address_id = request.POST.get('address_id')

    if not address_id:
        res_body = {
            "error": "address_id not provided"
        }
        return JsonResponse(res_body, status=400)

    user_address = get_object_or_404(user.addresses, pk=address_id)
    user_address.delete()

    res_body = {
        "success": "{}'s such address successfully removed".format(user.get_full_name())
    }
    return JsonResponse(res_body)
