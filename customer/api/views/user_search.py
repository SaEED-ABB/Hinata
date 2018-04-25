from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api
from customer.models import User

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
@check_permission_api(['admin'])
def user_search(request):
    try:
        username = request.GET.get('username')
        if not username:
            res_body = {
                "error": "Bad Request"
            }
            return JsonResponse(res_body, status=400)

        context = []
        for i in User.objects.filter(username__icontains=username):
            context.append({
                "full_name": i.get_full_name(),
                "username": i.username,
                "national_code": i.national_code,
            })
        return JsonResponse(context, safe=False)
    except:
        res_body = {
            "error": "Bad Request"
        }
        return JsonResponse(res_body, status=400)
