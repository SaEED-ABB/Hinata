from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from store.models import Product, Color, Size, ProductImage
from customer.models import Comment, Basket, SelectedProduct
from ratelimit.decorators import ratelimit


@require_http_methods(['GET'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
def get_product_info(request):
    """
    get a product info
    :param request: user, product_slug
    :return: product{name, price, properties[{name}], tags[{tag_name}], material, category,
            colors[{name, code}], sizes[{name}], comments[{comment, full_name, phone_number, created_at}],
            images[{url}], is_in_user_favorites, is_in_user_active_basket}
    """

    product_slug = request.GET.get('product_slug')
    if not product_slug:
        res_body = {
            "error": "product_slug not provided"
        }
        return JsonResponse(res_body, status=400)

    try:
        product = Product.objects.get(slug=product_slug)
    except Product.DoesNotExist:
        res_body = {
            "error": "no such product"
        }
        return JsonResponse(res_body, status=404)

    context = {
        "name": product.name,
        "slug": product.slug,
        "price": product.price,
        "properties": [],
        "tags": [],
        "material": product.material if product.material else "",
        "category": product.category.name if product.category else "",
        "colors": [],
        "sizes": [],
        "comments": [],
        "images": [],
        "average_rate": product.get_rates_average()
    }

    user = request.user
    if user.is_authenticated:
        context["is_in_user_favorites"] = product in user.favorites.all()
        context["is_in_user_active_basket"] = SelectedProduct.objects.filter(basket__user=user, basket__status=Basket.OPEN_CHECKING, product=product).exists()

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
            "slug": color.slug
        })

    for size in product.sizes.all():
        context['sizes'].append({
            "name": size.name,
            "slug": size.slug
        })

    for comment in Comment.objects.filter(product=product, is_approved=True):
        if comment.is_approved:
            if comment.user:
                user_name = comment.user.get_full_name()
                if comment.user.profile_picture:
                    user_photo_url = comment.user.profile_picture.url
                else:
                    user_photo_url = ""
            else:
                user_name = comment.session_name
                user_photo_url = ""

            context['comments'].append({
                "comment": comment.comment,
                "name": user_name,
                "user_photo_url": user_photo_url,
                "created_at": comment.created_at
            })

    for image in ProductImage.objects.filter(product=product):
        context['images'].append({
            image.name: image.image.url
        })

    return JsonResponse(context, safe=False, status=200)
