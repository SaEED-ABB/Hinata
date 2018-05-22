from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

from customer.decorators import check_permission_api
from store.models import Product

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def add_favorite(request):
    """
    user selects a product as its favorite and it will be add to his favorites list
    :param request: user, product_slug
    :return: error or success message
    """
    user = request.user
    product_slug = request.POST.get('product_slug')

    if not product_slug:
        res_body = {
            "error": "product_slug not provided"
        }
        return JsonResponse(res_body, status=400)

    try:
        this_product = Product.objects.get(slug=product_slug)
        user.favorites.add(this_product)

    except Product.DoesNotExist:
        res_body = {
            "error": "no such product"
        }
        return JsonResponse(res_body, status=404)

    res_body = {
        "success": "Favorite product successfully added for {}".format(user.get_full_name())
    }
    return JsonResponse(res_body, status=201)
