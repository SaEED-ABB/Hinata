from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from ratelimit.decorators import ratelimit

from store.models import Product, Category, ProductTags
from customer.models import Basket, SelectedProduct


@require_http_methods(['GET'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
def get_products(request):
    """
    returns all products [with specific category and tags]
    :param request: user, page, count, category_slug, tag_slug
    :return: products[{slug, name, price, front_image, back_image, is_in_user_favorites, is_in_user_active_basket}]
    """

    user = request.user

    this_page_number = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '12'))
    category_slug = request.GET.get('category_slug')
    tag_slug = request.GET.get('tag_slug')

    all_products = Product.objects.all()

    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            all_products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            res_body = {
                "error": "no such category"
            }
            return JsonResponse(res_body, status=404)

    if tag_slug:
        try:
            tag = ProductTags.objects.get(tag_name=tag_slug)
            all_products = all_products.filter(tags_in=tag)
        except ProductTags.DoesNotExist:
            res_body = {
                "error": "no such product_tag"
            }
            return JsonResponse(res_body, status=404)

    all_pages = Paginator(all_products, count)
    print(all_pages)
    requested_page = all_pages.page(this_page_number)
    print(requested_page)
    context = {
        "products": [],
        "more": requested_page.has_next(),
        "count": count if requested_page.has_next() else all_products.count() % count,
        # "next": requested_page.has_next(),
        # "previous": requested_page.has_previous(),
    }
    # if context["next"]:
    #     context["next_page_number"] = requested_page.next_page_number()
    # if context["previous"]:
    #     context["previous_page_number"] = requested_page.previous_page_number()

    for p in requested_page.object_list:
        front_image = p.images.filter(name='front').first()
        back_image = p.images.filter(name='back').first()

        is_in_user_active_basket = False
        is_in_user_favorites = False
        if not request.user.is_anonymous:
            is_in_user_favorites = p in user.favorites.all()
            is_in_user_active_basket = SelectedProduct.objects.filter(basket__user=user,
                                                                  basket__status=Basket.OPEN_CHECKING,
                                                                  product=p).exists()

        context['products'].append({
            "slug": p.slug,
            "name": p.name,
            "price": p.price,
            "front_image": front_image.image.url if front_image else "",
            "back_image": back_image.image.url if back_image else "",
            "is_in_user_active_basket": is_in_user_active_basket,
            "is_in_user_favorites": is_in_user_favorites
        })

    return JsonResponse(context, safe=False, status=200)
