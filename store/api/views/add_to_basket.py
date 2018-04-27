from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

from customer.models import Basket, SelectedProduct
from store.models import Product
from customer.decorators import check_authentication_status

from ratelimit.decorators import ratelimit


@require_http_methods(['POST'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@check_authentication_status()
def add_to_basket(request):

    this_user = request.user
    product_id = request.GET.get('product_id')
    # color_id = int(request.GET.get('color_id'))
    # size_id = int(request.GET.get('size_id'))
    count = int(request.GET.get('count', 1))

    if not product_id:
        res_body = {
            "error": "product_id not provided"
        }
        return JsonResponse(res_body, status=400)

    # try:
    #     this_color = this_product.colors.get(pk=color_id)
    # except ObjectDoesNotExist:
    #     res_body = {
    #         "error": "This product doesn't have this color"
    #     }
    #     return JsonResponse(res_body, status=400)
    #
    # try:
    #     this_size = this_product.sizes.get(pk=size_id)
    # except ObjectDoesNotExist:
    #     res_body = {
    #         "error": "This product doesn't have this size"
    #     }
    #     return JsonResponse(res_body, status=400)

    product = get_object_or_404(Product, pk=product_id)
    basket, created = Basket.objects.get_or_create(user=this_user, status='in_progress')
    
    selected_product, created = SelectedProduct.objects.get_or_create(
        basket=basket,
        product=product,
    )
    if created:
        selected_product.count = count
    else:
        selected_product.count += count

    selected_product.price = selected_product.count * product.price
    selected_product.save()

    res_body = {
        "success": "Such product successfully added to {}'s basket".format(this_user.get_full_name())
    }
    return JsonResponse(res_body)
