from json import loads as json_loads

from django.http.response import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api
from customer.models import User

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def change_password(request):
    try:
        request_body = request.body.decode('utf-8')
        data = json_loads(request_body)

        this_user = request.user
        # this_user = User.objects.get(pk=1)
        old_password = data['old_password']
        new_password = data['new_password']
        new_password_repeat = data['new_password_repeat']
    except:
        res_body = {
            "error": "Bad Request"
        }
        return JsonResponse(res_body, status=400)

    if not new_password == new_password_repeat:
        res_body = {
            "error": "The new passwords isn't equal"
        }
        return JsonResponse(res_body, status=400)

    if this_user.check_password(old_password):
        this_user.password = make_password(new_password)
        this_user.save()
        return JsonResponse({})
    else:
        res_body = {
            "error": "Old password is wrong"
        }
        return JsonResponse(res_body, status=400)
