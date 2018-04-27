from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='1000/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
@check_permission_api(['user'])
def get_favorite(request):

    user = request.user

    context = []
    for favorite_product in user.favorites.all():
        context.append({
            "product_name": favorite_product.name,
            "product_id": favorite_product.pk,
        })

    return JsonResponse(context, safe=False)
