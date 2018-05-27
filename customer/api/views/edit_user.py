from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_authentication_status

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_authentication_status()
def edit_user(request):
    """
    user can change his info
    :param request: user
    :return: error or success message
    """
    user = request.user

    phone_number = request.POST.get('phone_number')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    if not (phone_number and first_name and last_name):
        res_body = {
            "error": "phone_number or first_name or last_name not provided"
        }
        return JsonResponse(res_body, status=400)

    res_body, status = user.edit_yourself(phone_number=phone_number, first_name=first_name, last_name=last_name)
    return JsonResponse(res_body, status=status)
