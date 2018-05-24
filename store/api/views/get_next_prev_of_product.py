from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Count

from store.models import Product
from ratelimit.decorators import ratelimit

from store.models import FilterOption


@require_http_methods(['GET'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
def get_next_prev_of_product(request):

    product_slug = request.GET.get('product_slug')

    category_slug = request.GET.get('category_slug')

    filter_slug_sort_by = request.GET.get('filter_slug_sort_by')
    filter_option_slug_sort_by = request.GET.get('filter_option_slug_sort_by')
    filter_slug_1 = request.GET.get('filter_slug_1')
    filter_option_slug_1 = request.GET.get('filter_option_slug_1')
    filter_slug_2 = request.GET.get('filter_slug_2')
    filter_option_slug_2 = request.GET.get('filter_option_slug_2')

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

    # sooner_created = Product.objects.filter(created_at__lt=product.created_at).order_by('-created_at')
    # later_created = Product.objects.filter(created_at__gt=product.created_at).order_by('created_at')
    desired_products = Product.objects.all()
    next_pro = None
    prev_pro = None

    if category_slug:
        desired_products = desired_products.filter(category__slug=category_slug)

    if filter_slug_1 and filter_option_slug_1:
        option = FilterOption.objects.get(related_filter__slug=filter_slug_1, slug=filter_option_slug_1)
        desired_products = desired_products.filter(filter_options__name__in=option)
    if filter_slug_2 and filter_option_slug_2:
        option = FilterOption.objects.get(related_filter__slug=filter_slug_2, slug=filter_option_slug_2)
        desired_products = desired_products.filter(filter_options__name__in=option)

    if filter_slug_sort_by and filter_option_slug_sort_by:
        if filter_option_slug_sort_by == 'newest':
            next_pro = desired_products.filter(created_at__lt=product.created_at).order_by('-created_at').first()
            prev_pro = desired_products.filter(created_at__gt=product.created_at).order_by('created_at').first()
        elif filter_option_slug_sort_by == 'most-viewed':
            pass
        elif filter_option_slug_sort_by == 'most-favorite':
            next_pro = desired_products.annotate(lovers_count=Count('lovers')).filter(lovers_count__lte=product.lovers.count()).exclude(slug=product.slug).order_by('-lovers_count').first()
            prev_pro = desired_products.annotate(lovers_count=Count('lovers')).filter(lovers_count__gte=product.lovers.count()).exclude(slug=product.slug).order_by('lovers_count').first()
    else:
        next_pro = desired_products.filter(created_at__lt=product.created_at).order_by('-created_at').first()
        prev_pro = desired_products.filter(created_at__gt=product.created_at).order_by('created_at').first()

    context = {
    }
    if next_pro:
        context['next'] = {
            'link': next_pro.get_absolute_url(),
            'image': next_pro.images.filter(name='front').last().image.url if next_pro.images.exists() else "",
            'slug': next_pro.slug
        }
    if prev_pro:
        context['prev'] = {
            'link': prev_pro.get_absolute_url(),
            'image': prev_pro.images.filter(name='front').last().image.url if prev_pro.images.exists() else "",
            'slug': prev_pro.slug
        }

    return JsonResponse(context, status=200)
