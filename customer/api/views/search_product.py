from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from store.models import Product
from store.helpers import get_one_image

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
def search_product(request):

    search_key = request.GET.get('search_key')

    if not search_key:
        res_body = {
            "error": "search_key not provided"
        }
        return JsonResponse(res_body, status=400)

    context = []
    for product in Product.objects.filter(name__icontains=search_key):
        context.append({
            "name": product.name,
            "id": product.id,
            "image": get_one_image(product)
        })
    return JsonResponse(context, safe=False)
