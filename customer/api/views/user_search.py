from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api
from customer.models import User

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
@check_permission_api(['admin'])
def user_search(request):
    """
    admin searches for a specific user and his info
    :param request: phone_number
    :return: user{full_name, phone_number}
    """
    phone_number = request.GET.get('phone_number')
    if not phone_number:
        res_body = {
            "error": "phone_number not provided"
        }
        return JsonResponse(res_body, status=400)

    context = []
    for user in User.objects.filter(phone_number=phone_number):
        context.append({
            "full_name": user.get_full_name(),
            "phone_number": user.phone_number,
        })
    return JsonResponse(context, safe=False, status=200)
