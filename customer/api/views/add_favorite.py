
from json import loads as json_loads

from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api
from customer.models import Favorite, User
from store.models import Product

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def add_favorite(request):
    try:
        request_body = request.body.decode('utf-8')
        data = json_loads(request_body)

        # user = User.objects.get(pk=1)
        user = request.user
        product = data['product']
    except:
        res_body = {
            "error": "Bad Request"
        }
        return JsonResponse(res_body, status=400)

    try:
        this_product = Product.objects.get(pk=product)
    except Product.DoesNotExist:
        res_body = {
            "error": "Product not found"
        }
        return JsonResponse(res_body, status=400)

    this_favorite = Favorite()
    this_favorite.product = this_product
    this_favorite.user = user
    this_favorite.save()

    res_body = {
        "id": this_favorite.pk
    }
    return JsonResponse(res_body)
