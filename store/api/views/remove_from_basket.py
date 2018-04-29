from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
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

    product_id = request.POST.get('product_id')
    count = request.POST.get('count', 'all')

    if not product_id:
        res_body = {
            "error": "product_id not provided"
        }
        return JsonResponse(res_body, status=400)

    product = get_object_or_404(Product, pk=product_id)
    basket = get_object_or_404(Basket, user=this_user, status='in_progress')
    selected_product = get_object_or_404(SelectedProduct, product=product, basket=basket)

    if count == 'all' or int(count) >= selected_product.count:
        selected_product.delete()
    else:
        selected_product.count -= int(count)
        selected_product.save()

    res_body = {
        "success": "Such product successfully removed from {}'s basket".format(this_user.get_full_name())
    }
    return JsonResponse(res_body)