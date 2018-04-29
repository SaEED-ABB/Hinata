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

    user = request.user

    basket = get_object_or_404(Basket, user=user, status=Basket.OPEN_CHECKING)
    context = basket.get_info(all_colors_and_sizes_per_product=True)

    return JsonResponse(context, safe=False)
