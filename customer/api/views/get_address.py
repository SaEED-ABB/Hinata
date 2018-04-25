from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import Q

from customer.decorators import check_permission_api
from customer.models import UserAddress, User

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='1000/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
@check_permission_api(['user'])
def get_address(request):
    user = request.user
    # user = User.objects.get(pk=1)
    context = []
    for i in UserAddress.objects.filter(user=user):
        context.append({
            "address": i.address,
            "phone": i.phone_number,
            "id": i.pk
        })
    return JsonResponse(context, safe=False)
