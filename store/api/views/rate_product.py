from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from ratelimit.decorators import ratelimit

from customer.models import ProductRate
from store.models import Product
from customer.decorators import check_permission_api


@require_http_methods(['POST'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
# @check_permission_api(['user'])
def rate_product(request):

    product_slug = request.POST.get('product_slug')
    # rate = request.POST.get('rate')
    rate_fabric = request.POST.get('rate_fabric')
    rate_beauty = request.POST.get('rate_beauty')
    rate_manner = request.POST.get('rate_manner')
    rate_price = request.POST.get('rate_price')
    session_name = request.POST.get('session_name')

    if not (product_slug and rate_fabric and rate_beauty and rate_manner and rate_price):
        res_body = {
            "error": "product_slug or rates not provided"
        }
        return JsonResponse(res_body, status=400)

    if not (0 <= int(rate_fabric) <= 100 and 0 <= int(rate_beauty) <= 100 and 0 <= int(rate_manner) <= 100 and 0 <= int(rate_price) <= 100):
        res_body = {
            "error": "rate should be in range of 0 to 100"
        }
        return JsonResponse(res_body, status=400)

    try:
        product = Product.objects.get(slug=product_slug)
        user = request.user
        if user.is_authenticated:
            p_rate = product.rates.get_or_create(user=user)[0]
        else:
            if not session_name:
                res_body = {"error": "session_name not provided"}
                return JsonResponse(res_body, status=400)
            if not request.session.session_key:
                request.session.save()
            session_id = request.session.session_key
            p_rate = product.rates.get_or_create(session_id=session_id, session_name=session_name)[0]

        res_body, status = p_rate.update_yourself(rate_fabric=int(rate_fabric),
                                                  rate_beauty=int(rate_beauty),
                                                  rate_manner=int(rate_manner),
                                                  rate_price=int(rate_price))
    except Product.DoesNotExist:
        res_body = {
            "error": "no such product"
        }
        status = 404

    return JsonResponse(res_body, status=status)
