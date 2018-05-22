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
    """
    add a comment for a specific product left by current user
    :param request: user, product_slug, comment
    :return: error or success message
    """

    user = request.user
    product_slug = request.POST.get('product_slug')
    comment = request.POST.get('comment')

    if not (product_slug and comment):
        res_body = {
            "error": "product_slug or comment not provided"
        }
        return JsonResponse(res_body, status=400)

    try:
        this_product = Product.objects.get(slug=product_slug)
    except Product.DoesNotExist:
        res_body = {
            "error": "no such product"
        }
        return JsonResponse(res_body, status=404)

    Comment.objects.create(comment=comment, product=this_product, user=user)

    res_body = {
        "success": "Comment for such product added successfully for {}".format(user.get_full_name())
    }
    return JsonResponse(res_body, status=201)
