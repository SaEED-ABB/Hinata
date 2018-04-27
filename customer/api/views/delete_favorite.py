from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

from customer.decorators import check_permission_api
from store.models import Product

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def delete_favorite(request):

    user = request.user
    product_id = request.GET.get('product_id')

    if not product_id:
        res_body = {
            "error": "product_id not provided"
        }
        return JsonResponse(res_body, status=400)

    favorite_product = get_object_or_404(Product, id=product_id)
    user.favorites.remove(favorite_product)

    res_body = {
        "success": "{}'s such favorite product removed successfully from his favorites"
    }
    return JsonResponse(res_body)
