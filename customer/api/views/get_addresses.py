from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='1000/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
@check_permission_api(['user'])
def get_addresses(request):
    """
    returns all user addresses
    :param request: user
    :return: addresses[{address, phone, id}]
    """
    user = request.user

    context = user.get_addresses()

    return JsonResponse(context, safe=False, status=200)
