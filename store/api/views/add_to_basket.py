from json import loads as json_loads

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
def add_to_basket(request):
    try:
        # request_body = request.body.decode('utf-8')
        # data = json_loads(request_body)

        # this_user = User.objects.get(pk=1)
        this_user = request.user
        product_id = int(request.GET.get('product_id'))
        color_id = int(request.GET.get('color_id'))
        size_id = int(request.GET.get('size_id'))
        count = int(request.GET.get('count', 1))
    except:
        res_body = {
            "error": "Bad Request"
        }
        return JsonResponse(res_body, status=400)

    this_product = get_object_or_404(Product, pk=product_id)
    print(this_product)
    try:
        this_color = this_product.colors.get(pk=color_id)
    except ObjectDoesNotExist:
        res_body = {
            "error": "This product doesn't have this color"
        }
        return JsonResponse(res_body, status=400)

    try:
        this_size = this_product.sizes.get(pk=size_id)
    except ObjectDoesNotExist:
        res_body = {
            "error": "This product doesn't have this size"
        }
        return JsonResponse(res_body, status=400)

    this_basket, created = Basket.objects.get_or_create(user=this_user, status='in_progress')
    
    this_selected_product, created = SelectedProduct.objects.get_or_create(
        basket=this_basket,
        product=this_product,
        color=this_color,
        size=this_size
    )
    if created:
        this_selected_product.count = count
    else:
        this_selected_product.count += count
    this_selected_product.price = str(
        this_product.price * this_selected_product.count
    )
    this_selected_product.save()

    res_body = {
        "id": str(this_selected_product.pk)
    }
    return JsonResponse(res_body)
