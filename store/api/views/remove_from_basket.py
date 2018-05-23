from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

from customer.models import Basket, SelectedProduct, User
from store.models import Product
from customer.decorators import check_authentication_status

from ratelimit.decorators import ratelimit


@require_http_methods(['POST'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@check_authentication_status()
def remove_from_basket(request):
    """
    a user can remove a specific product from his active basket
    :param request:
    :return:
    """
    user = request.user

    product_slug = request.POST.get('product_slug')
    count = request.POST.get('count', 'all')

    if not product_slug:
        res_body = {
            "error": "product_slug not provided"
        }
        return JsonResponse(res_body, status=400)

    try:
        basket = user.baskets.get(status=Basket.OPEN_CHECKING)
        res_body, status = basket.remove_product_from_yourself(product_slug, count)
    except Basket.DoesNotExist:
        res_body = {"error": "no active basket found for user {}".format(user.get_full_name())}
        status = 400

    return JsonResponse(res_body, status=status)

