from json import loads as json_loads

from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api
from customer.models import Favorite, User

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def delete_favorite(request):
    try:
        request_body = request.body.decode('utf-8')
        data = json_loads(request_body)

        # user = User.objects.get(pk=1)
        user = request.user
        favorite_id = data['favorite']
    except:
        res_body = {
            "error": "Bad Request"
        }
        return JsonResponse(res_body, status=400)

    this_favorite = Favorite.objects.filter(pk=favorite_id, user=user)
    if not this_favorite:
        res_body = {
            "error": "Favorite does not exists"
        }
        return JsonResponse(res_body, status=400)

    this_favorite.delete()
    return JsonResponse({})
