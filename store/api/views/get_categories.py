from json import loads as json_loads

from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models.query import Q

from store.models import Category
from ratelimit.decorators import ratelimit


@require_http_methods(['GET'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
def get_categories(request):
    # try:
        all_categories = []
        for i in Category.objects.filter(parent=None):
            childrens = []
            for j in Category.objects.filter(parent=i):
                childrens.append({
                    "name": j.name,
                    "id": j.id
                })
            all_categories.append({
                "name": i.name,
                "id": i.id,
                "children": childrens
            })
        return JsonResponse(all_categories, safe=False)
    # except:
    #     res_body = {
    #         "error": "Bad Request"
    #     }
    #     return JsonResponse(res_body, status=400)
