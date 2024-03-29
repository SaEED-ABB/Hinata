from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models.query import Q
from django.shortcuts import get_object_or_404

from customer.decorators import check_permission_api
from customer.models import Basket

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='1000/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
@check_permission_api(['user'])
def get_active_basket_info(request):
    """
    each user has one and only one active basket which its info is returned by this api
    :param request: user, basket
    :return: total_price, status, products[{name, image, id, desired_color, desired_size, count, price,
            colors[{name, color}], sizes[{name}], }]
    """
    user = request.user

    try:
        basket = Basket.objects.get(user=user, status=Basket.OPEN_CHECKING)
        context = basket.get_info(all_colors_and_sizes_per_product=True)
    except Basket.DoesNotExist:
        res_body = {
            "error": "no such active basket found for {}".format(user.get_full_name())
        }
        return JsonResponse(res_body, status=404)

    return JsonResponse(context, safe=False, status=200)
