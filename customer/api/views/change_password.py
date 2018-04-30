from django.http.response import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def change_password(request):
    """
    user can change his password
    :param request: old_password, new_password, new_password_confirm
    :return: error or success message
    """
    this_user = request.user

    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    new_password_confirm = request.POST.get('new_password_confirm')

    if not (old_password and new_password and new_password_confirm):
        res_body = {
            "error": "old_password or new_password or new_password_confirm not provided"
        }
        return JsonResponse(res_body, status=400)

    if not new_password == new_password_confirm:
        res_body = {
            "error": "New password confirm does not match"
        }
        return JsonResponse(res_body, status=400)

    if this_user.check_password(old_password):
        this_user.password = make_password(new_password)
        this_user.save()
        update_session_auth_hash(request, this_user)
        res_body = {
            "success": "{}'s password changed successfully".format(this_user.get_full_name())
        }
        return JsonResponse(res_body, status=201)
    else:
        res_body = {
            "error": "Password provided is incorrect"
        }
        return JsonResponse(res_body, status=400)
