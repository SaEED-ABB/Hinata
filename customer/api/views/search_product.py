from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from store.models import Product

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['GET'])
def search_product(request):
    """
    search among product names
    :param request: search_key
    :return: product{name, id, image}
    """
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
            "slug": product.slug,
            "image": product.images.last().image.url
        })
    return JsonResponse(context, safe=False, status=200)
