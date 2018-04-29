from django.shortcuts import get_object_or_404
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

    user = request.user
    product_id = request.POST.get('product_id')
    comment = request.POST.get('comment')

    if not (product_id and comment):
        res_body = {
            "error": "product_id or comment not provided"
        }
        return JsonResponse(res_body, status=400)

    this_product = get_object_or_404(Product, pk=product_id)

    Comment.objects.create(comment=comment, product=this_product, user=user)

    res_body = {
        "success": "Comment for such product added successfully for {}".format(user.get_full_name())
    }
    return JsonResponse(res_body)
