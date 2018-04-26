from json import loads as json_loads

from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from store.models import Product, Category
from ratelimit.decorators import ratelimit


@require_http_methods(['GET'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
def get_products(request):
    # try:
    this_page_number = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '12'))

    category = get_object_or_404(Category, name=request.GET.get('category'))
    all_products = Product.objects.filter(category=category)
    all_pages = Paginator(all_products, count)
    requested_page = all_pages.page(this_page_number)
    context = {
        "products": [],
        "more": True if all_products.count() > count else False,
        "next": requested_page.has_next(),
        "previous": requested_page.has_previous(),
        "count": all_pages.count()
    }
    if context["next"]:
        context["next_page_number"] = requested_page.next_page_number()
    if context["previous"]:
        context["previous_page_number"] = requested_page.previous_page_number()

    for i in requested_page.object_list:
        context['products'].append({
            "name": i.name,
            "price": i.price,
        })

    return JsonResponse(context, safe=False)
    # except:
    #     res_body = {
    #         "error": "Bad Request"
    #     }
    #     return JsonResponse(res_body, status=400)
