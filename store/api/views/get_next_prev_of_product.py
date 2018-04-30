from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from store.models import Product
from ratelimit.decorators import ratelimit


@require_http_methods(['GET'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
def get_next_prev_of_product(request):

    product_id = request.GET.get('product_id')

    if not product_id:
        res_body = {
            "error": "product_id not provided"
        }
        return JsonResponse(res_body, status=400)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        res_body = {
            "error": "no such product"
        }
        return JsonResponse(res_body, status=404)

    sooner_created = Product.objects.filter(created_at__lt=product.created_at).order_by('-created_at')
    later_created = Product.objects.filter(created_at__gt=product.created_at).order_by('created_at')
    # sooner_created = product.get_previous_by_created_at()
    # later_created = product.get_next_by_created_at()

    context = {
    }
    if later_created.exists():
        context['next'] = {
            'link': later_created[0].get_absolute_url(),
            'image': later_created[0].images.last().image.url if later_created[0].images.exists() else "",
            'id': later_created[0].pk
        }
    if sooner_created.exists():
        context['prev'] = {
            'link': sooner_created[0].get_absolute_url(),
            'image': sooner_created[0].images.last().image.url if sooner_created[0].images.exists() else "",
            'id': sooner_created[0].pk
        }

    return JsonResponse(context, status=200)
