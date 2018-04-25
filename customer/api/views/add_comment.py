from json import loads as json_loads

from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api
from customer.models import Comment, User
from store.models import Product

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
@check_permission_api(['user'])
def add_comment(request):
    try:
        request_body = request.body.decode('utf-8')
        data = json_loads(request_body)

        # user = User.objects.get(pk=1)
        user = request.user
        product = data['product']
        comment = data['comment']
    except:
        res_body = {
            "error": "Bad Request"
        }
        return JsonResponse(res_body, status=400)

    try:
        this_product = Product.objects.get(pk=product)
    except Product.DoesNotExist:
        res_body = {
            "error": "Product not found"
        }
        return JsonResponse(res_body, status=400)

    this_comment = Comment()
    this_comment.comment = comment
    this_comment.product = this_product
    this_comment.user = user
    this_comment.save()

    res_body = {
        "id": this_comment.pk
    }
    return JsonResponse(res_body)
