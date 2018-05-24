from django.db.models import Count
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from ratelimit.decorators import ratelimit

from store.models import Product, Category, ProductTags, FilterOption
from customer.models import Basket, SelectedProduct


@require_http_methods(['GET'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
def get_products(request):
    """
    returns all products [with specific category and tags]
    :param request: user, page, count, category_slug, tag_slug
    :return: products[{slug, name, price, front_image, back_image, is_in_user_favorites, is_in_user_active_basket}]
    """

    this_page_number = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '12'))
    category_slug = request.GET.get('category_slug')
    tag_slug = request.GET.get('tag_slug')

    filter_slug_sort_by = request.GET.get('filter_slug_sort_by')
    filter_option_slug_sort_by = request.GET.get('filter_option_slug_sort_by')
    filter_slug_1 = request.GET.get('filter_slug_1')
    filter_option_slug_1 = request.GET.get('filter_option_slug_1')
    filter_slug_2 = request.GET.get('filter_slug_2')
    filter_option_slug_2 = request.GET.get('filter_option_slug_2')

    desired_products = Product.objects.all()

    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            desired_products = desired_products.filter(category=category)
        except Category.DoesNotExist:
            res_body = {
                "error": "no such category"
            }
            return JsonResponse(res_body, status=404)

    if tag_slug:
        try:
            tag = ProductTags.objects.get(tag_name=tag_slug)
            desired_products = desired_products.filter(tags_in=tag)
        except ProductTags.DoesNotExist:
            res_body = {
                "error": "no such product_tag"
            }
            return JsonResponse(res_body, status=404)

    if filter_slug_1 and filter_option_slug_1:
        option = FilterOption.objects.get(related_filter__slug=filter_slug_1, slug=filter_option_slug_1)
        desired_products = desired_products.filter(filter_options__name__in=option)
    if filter_slug_2 and filter_option_slug_2:
        option = FilterOption.objects.get(related_filter__slug=filter_slug_2, slug=filter_option_slug_2)
        desired_products = desired_products.filter(filter_options__name__in=option)

    if filter_slug_sort_by and filter_option_slug_sort_by:
        if filter_option_slug_sort_by == 'newest':
            desired_products = desired_products.order_by('-created_at')
        elif filter_option_slug_sort_by == 'most-viewed':
            pass
        elif filter_option_slug_sort_by == 'most-favorite':
            desired_products = desired_products.annotate(lovers_count=Count('lovers')).order_by('-lovers_count')
    else:
        desired_products = desired_products.order_by('-created_at')

    all_pages = Paginator(desired_products, count)

    print(all_pages)
    requested_page = all_pages.page(this_page_number)
    print(requested_page)
    context = {
        "products": [],
        "more": requested_page.has_next(),
        "count": count if requested_page.has_next() else desired_products.count() % count,
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

        context_products_value = {
            # "lovers": p.lovers.count(),
            "slug": p.slug,
            "name": p.name,
            "price": p.price,
            "front_image": front_image.image.url if front_image else "",
            "back_image": back_image.image.url if back_image else "",
        }
        user = request.user
        if user.is_authenticated:
            is_in_user_favorites = p in user.favorites.all()
            is_in_user_active_basket = SelectedProduct.objects.filter(basket__user=user, basket__status=Basket.OPEN_CHECKING, product=p).exists()
            context_products_value["is_in_user_active_basket"] = is_in_user_active_basket
            context_products_value["is_in_user_favorites"] = is_in_user_favorites

        context['products'].append(context_products_value)

    return JsonResponse(context, safe=False, status=200)
