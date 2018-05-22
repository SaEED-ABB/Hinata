from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from store.models import Category
from ratelimit.decorators import ratelimit


@require_http_methods(['GET'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
def get_categories(request):
    """
    we have a 2 level categories for products for now
    :param request:
    :return: categories[{name, slug, children}]
    """
    all_categories = []
    for i in Category.objects.filter(parent=None):
        childrens = []
        for j in Category.objects.filter(parent=i):
            childrens.append({
                "name": j.name,
                "slug": j.slug
            })
        all_categories.append({
            "name": i.name,
            "slug": i.slug,
            "children": childrens
        })
    return JsonResponse(all_categories, safe=False, status=200)
