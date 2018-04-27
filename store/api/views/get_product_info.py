from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from store.models import Product, Color, Size, ProductImage
from customer.models import Comment
from ratelimit.decorators import ratelimit


@require_http_methods(['GET'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
def get_product_info(request):

    this_product_id = request.GET.get('product_id')
    if not this_product_id:
        res_body = {
            "error": "product_id not provided"
        }
        return JsonResponse(res_body, status=400)

    this_product = get_object_or_404(Product, pk=this_product_id)

    context = {
        "name": this_product.name,
        "price": this_product.price,
        "properties": [],
        "material": this_product.material,
        "category": this_product.category.name if this_product.category else "",
        "colors": [],
        "sizes": [],
        "comments": [],
        "images": []
    }

    for i in this_product.properties.all():
        context['properties'].append({
            "property": i.property
        })

    for i in this_product.colors.all():
        context['colors'].append({
            "name": i.name,
            "color_code": i.color,
            "id": i.pk
        })

    for i in this_product.sizes.all():
        context['sizes'].append({
            "name": i.name,
            "id": i.pk
        })

    for i in Comment.objects.filter(product=this_product, is_approved=True):
        context['comments'].append({
            "comment": i.comment,
            "username": i.user.username,
            "full_name": i.user.get_full_name(),
            "created_at": i.created_at
        })

    for i in ProductImage.objects.filter(product=this_product):
        context['images'].append({
            "url": i.image.image.url
        })

    return JsonResponse(context, safe=False)
