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

    product_id = request.GET.get('product_id')
    if not product_id:
        res_body = {
            "error": "product_id not provided"
        }
        return JsonResponse(res_body, status=400)

    product = get_object_or_404(Product, pk=product_id)

    context = {
        "name": product.name,
        "price": product.price,
        "properties": [],
        "tags": [],
        "material": product.material,
        "category": product.category.name if product.category else "",
        "colors": [],
        "sizes": [],
        "comments": [],
        "images": []
    }

    for property in product.properties.all():
        context['properties'].append({
            "property": property.property
        })

    for tag in product.tags.all():
        context['tags'].append({
            "tag": tag.tag_name
        })

    for color in product.colors.all():
        context['colors'].append({
            "name": color.name,
            "color_code": color.color,
            "id": color.pk
        })

    for size in product.sizes.all():
        context['sizes'].append({
            "name": size.name,
            "id": size.pk
        })

    for comment in Comment.objects.filter(product=product, is_approved=True):
        context['comments'].append({
            "comment": comment.comment,
            "phone_number": comment.user.phone_number,
            "full_name": comment.user.get_full_name(),
            "created_at": comment.created_at
        })

    for image in ProductImage.objects.filter(product=product):
        context['images'].append({
            image.name: image.image.image.url
        })

    return JsonResponse(context, safe=False)
