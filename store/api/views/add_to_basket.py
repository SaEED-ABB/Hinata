from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

from customer.models import Basket, SelectedProduct
from store.models import Product, Color, Size
from customer.decorators import check_authentication_status

from ratelimit.decorators import ratelimit


@require_http_methods(['POST'])
@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@check_authentication_status()
def add_to_basket(request):
    """
    a user can add each of the products to his basket
    :param request: user, product_id, count=1, color_id="", size_id=""
    :return:
    """
    this_user = request.user
    product_id = request.POST.get('product_id')
    color_id = int(request.POST.get('color_id'))
    size_id = int(request.POST.get('size_id'))
    count = int(request.POST.get('count', 1))

    if not product_id:
        res_body = {
            "error": "product_id not provided"
        }
        return JsonResponse(res_body, status=400)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        res_body = {
            "error": "no such product"
        }
        return JsonResponse(res_body, status=404)

    basket, created_basket = Basket.objects.get_or_create(user=this_user, status=Basket.OPEN_CHECKING)

    selected_product, created_sel_product = SelectedProduct.objects.get_or_create(
        basket=basket,
        product=product,
    )
    if color_id:
        try:
            color = Color.objects.get(pk=color_id)
            selected_product.color = color
        except Color.DoesNotExist:
            res_body = {
                "error": "no such color"
            }
            return JsonResponse(res_body, status=404)

    if size_id:
        try:
            size = Size.objects.get(pk=size_id)
            selected_product.size = size
        except Size.DoesNotExist:
            res_body = {
                "error": "no such size"
            }
            return JsonResponse(res_body, status=404)

    if created_sel_product:
        selected_product.count = count
    else:
        selected_product.count += count

    selected_product.price = selected_product.count * product.price
    selected_product.save()

    if created_basket:
        basket.total_price = 0
    else:
        basket.total_price += selected_product.price
    basket.save()

    res_body = {
        "success": "Such product successfully added to {}'s basket".format(this_user.get_full_name())
    }
    return JsonResponse(res_body, status=201)
