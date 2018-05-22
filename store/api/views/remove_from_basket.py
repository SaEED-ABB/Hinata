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
    """
    a user can remove a specific product from his active basket
    :param request:
    :return:
    """
    this_user = request.user

    product_slug = request.POST.get('product_slug')
    count = request.POST.get('count', 'all')

    if not product_slug:
        res_body = {
            "error": "product_slug not provided"
        }
        return JsonResponse(res_body, status=400)

    try:
        product = Product.objects.get(slug=product_slug)
        basket = Basket.objects.get(user=this_user, status=Basket.OPEN_CHECKING)
        selected_product = SelectedProduct.objects.get(product=product, basket=basket)
    except (Product.DoesNotExist, SelectedProduct.DoesNotExist):
        res_body = {
            "error": "no such product"
        }
        return JsonResponse(res_body, status=404)
    except Basket.DoesNotExist:
        res_body = {
            "error": "no such active basket found for user {}".format(this_user.get_full_name())
        }
        return JsonResponse(res_body, status=404)

    if count == 'all' or int(count) >= selected_product.count:
        basket.total_price -= selected_product.price
        basket.save()
        selected_product.delete()
    else:
        selected_product.count -= int(count)
        selected_product.price -= int(count) * product.price
        selected_product.save()

        basket.total_price -= int(count) * product.price
        basket.save()

    res_body = {
        "success": "Such product successfully removed from {}'s basket".format(this_user.get_full_name())
    }
    return JsonResponse(res_body, status=204)