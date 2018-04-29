from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from ratelimit.decorators import ratelimit

from store.models import Product, Category, ProductTags


@require_http_methods(['GET'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
def get_products(request):
    user = request.user

    this_page_number = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '12'))
    category_name = request.GET.get('category')
    tag_name = request.GET.get('tag')

    if not category_name:
        res_body = {
            "error": "category_name not provided"
        }
        return JsonResponse(res_body, status=400)

    category = get_object_or_404(Category, name=category_name)
    all_products = Product.objects.filter(category=category)
    if tag_name:
        tag = get_object_or_404(ProductTags, tag_name=tag_name)
        all_products = all_products.filter(tags__id=tag.pk)
    all_pages = Paginator(all_products, count)
    requested_page = all_pages.page(this_page_number)
    context = {
        "products": [],
        "more": True if all_products.count() > count else False,
        "count": all_pages.count,
        # "next": requested_page.has_next(),
        # "previous": requested_page.has_previous(),
    }
    # if context["next"]:
    #     context["next_page_number"] = requested_page.next_page_number()
    # if context["previous"]:
    #     context["previous_page_number"] = requested_page.previous_page_number()

    for p in requested_page.object_list:
        front_image_url = get_object_or_404(p.images, name='front').image.url
        back_image_url = get_object_or_404(p.images, name='back').image.url

        is_in_basket = False
        is_favorite = False
        if not request.user.is_anonymous:
            is_in_basket = False
            basket = user.baskets.filter(status='in_progress')
            if basket.exists() and basket[0].selected_products.filter(product=p).exists():
                is_in_basket = True

            is_favorite = True if p in user.favorites.all() else False

        context['products'].append({
            "id": p.pk,
            "name": p.name,
            "price": p.price,
            "front_image": front_image_url,
            "back_image": back_image_url,
            "is_in_basket": is_in_basket,
            "is_favorite": is_favorite
        })

    return JsonResponse(context, safe=False)
