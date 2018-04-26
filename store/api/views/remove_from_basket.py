from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from customer.models import Basket, SelectedProduct, User
from store.models import Product
from customer.decorators import check_authentication_status

from ratelimit.decorators import ratelimit


@require_http_methods(['POST'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@check_authentication_status()
def remove_from_basket(request):
    this_user = request.user
    product_id = request.GET.get('product_id')
    count = request.GET.get('count', 'all')

    product = get_object_or_404(Product, pk=product_id)
    basket = get_object_or_404(Basket, user=this_user, status='in_progress')
    selected_product = get_object_or_404(SelectedProduct, product=product, basket=basket)

    if count == 'all' or int(count) >= selected_product.count:
        # basket.selected_products.remove(selected_product)
        selected_product.delete()
    else:
        selected_product.count -= int(count)
        selected_product.save()

    return JsonResponse({})