from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models.query import Q

from customer.decorators import check_permission_api
from customer.models import Basket

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='1000/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
@check_permission_api(['user'])
def get_basket_history(request):
    """
    among closed and open status basket all will return but the Basket.OPEN_CHECKING
    :param request: user
    :return: closed[{basket.get_info}], open[{basket.get_info}]
    """
    user = request.user

    context = {
        "closed": [],
        "open": []
    }

    for closed_basket in Basket.objects.filter(Q(status__istartswith='closed'), user=user):
        context["closed"].append(
            closed_basket.get_info()
        )

    for open_basket in Basket.objects.filter(~Q(status=Basket.OPEN_CHECKING), Q(status__istartswith='open'), user=user):
        context["open"].append(
            open_basket.get_info()
        )

    return JsonResponse(context, safe=False, status=200)
