from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import Q

from customer.decorators import check_permission_api
from customer.models import Basket, User
from store.helpers import total_price, get_selected_products

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='1000/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
@check_permission_api(['user'])
def get_history(request):
    user = request.user
    # user = User.objects.get(pk=1)
    context = []
    for i in Basket.objects.filter(~Q(status='in_progress'), user=user):
        context.append({
            "code": i.code,
            "updated_at": i.updated_at,
            "total_price": total_price(i),
            "status": i.status,
            "products": get_selected_products(i),
        })
    return JsonResponse(context, safe=False)
