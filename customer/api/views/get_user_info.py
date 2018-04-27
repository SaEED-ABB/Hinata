from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api
from customer.models import User

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='1000/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
@check_permission_api(['user'])
def get_user_info(request):
    # request.user = User.objects.get(pk=1)
    user = request.user
    context = {
        "phone_number": user.phone_number,
        "first_name": user.first_name,
        "last_name": user.last_name
    }
    return JsonResponse(context, safe=False)
