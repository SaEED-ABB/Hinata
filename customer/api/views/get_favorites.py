from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='1000/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
@check_permission_api(['user'])
def get_favorite(request):
    """
    each user has a favorite product list which could be returned
    :param request: user
    :return: favorites[images[{url}], product_name, product_id, price]
    """
    user = request.user

    context = user.get_favorites()

    return JsonResponse(context, safe=False, status=200)
