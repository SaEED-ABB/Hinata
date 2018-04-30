from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def edit_user(request):
    """
    user can change his info
    :param request: user
    :return: error or success message
    """
    this_user = request.user

    phone_number = request.POST.get('phone_number')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    if not (phone_number and first_name and last_name):
        res_body = {
            "error": "phone_number or first_name or last_name not provided"
        }
        return JsonResponse(res_body, status=400)

    this_user.phone_number = phone_number
    this_user.first_name = first_name
    this_user.last_name = last_name
    this_user.save()

    res_body = {
        "success": "User successfully updated"
    }
    return JsonResponse(res_body, status=201)
