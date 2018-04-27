from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='1000/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
@check_permission_api(['user'])
def get_address(request):

    user = request.user

    context = []
    for user_addr in user.addresses.all():
        context.append({
            "address": user_addr.address,
            "phone": user_addr.phone_number,
            "id": user_addr.pk
        })

    return JsonResponse(context, safe=False)
