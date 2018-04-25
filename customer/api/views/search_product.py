from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from store.models import Product, ProductImage
from store.helpers import get_one_image

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
def search_product(request):
    try:
        search_key = request.GET['search_key']
    except:
        res_body = {
            "error": "Bad Request"
        }
        return JsonResponse(res_body, status=400)

    context = []
    for i in Product.objects.filter(name__icontains=search_key):
        context.append({
            "name": i.name,
            "id": i.id,
            "image": get_one_image(i)
        })
    return JsonResponse(context, safe=False)
