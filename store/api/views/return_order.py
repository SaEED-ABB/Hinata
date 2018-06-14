from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from ratelimit.decorators import ratelimit

from customer.models import Basket
from customer.decorators import check_permission_api


@require_http_methods(['POST'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@check_permission_api(['user'])
def return_order(request):
    basket_code = request.POST.get('basket_code')

    try:
        basket = Basket.objects.get(code=basket_code)
    except Basket.DoesNotExist:
        res_body = {
            "error": "no such basket found for user {}".format(request.user.get_full_name())
        }
        return JsonResponse(res_body, status=404)

    if request.user != basket.user:
        res_body = {
            "error": "permission denied. request.user is not the same as basket.user"
        }
        return JsonResponse(res_body, status=403)

    res_body, status = basket.return_this_order()

    return JsonResponse(res_body, status)