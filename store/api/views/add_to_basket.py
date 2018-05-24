from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from ratelimit.decorators import ratelimit

from customer.models import Basket
from customer.decorators import check_permission_api


@require_http_methods(['POST'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@check_permission_api(['user'])
def add_to_basket(request):
    """
    a user can add each of the products to his basket
    :param request: user, product_slug, count=1, color_slug="", size_slug=""
    :return:
    """
    user = request.user
    product_slug = request.POST.get('product_slug')
    color_slug = request.POST.get('color_slug')
    size_slug = request.POST.get('size_slug')
    count = int(request.POST.get('count', 1))

    if not product_slug:
        res_body = {
            "error": "product_slug not provided"
        }
        return JsonResponse(res_body, status=400)

    basket = Basket.objects.get_or_create(user=user, status=Basket.OPEN_CHECKING)[0]

    res_body, status = basket.add_product_to_yourself(product_slug=product_slug,
                                                      color_slug=color_slug,
                                                      size_slug=size_slug,
                                                      count=count)
    return JsonResponse(res_body, status=status)
