from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods

from customer.decorators import check_permission_api
from customer.models import Comment

from ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='500/h', method=ratelimit.ALL, block=True)
@require_http_methods(['POST'])
# @check_permission_api(['user'])
def delete_comment(request):
    """
    user can delete each of his comments
    :param request: user, comment_id
    :return: error or success message
    """
    comment_id = request.POST.get('comment_id')

    if not comment_id:
        res_body = {
            "error": "comment_id not provided"
        }
        return JsonResponse(res_body, status=400)

    try:
        this_comment = Comment.objects.get(pk=comment_id)
        this_comment.delete()
    except Comment.DoesNotExist:
        res_body = {
            "error": "no such comment found on product"
        }
        return JsonResponse(res_body, status=404)

    if this_comment.user:
        res_body = {
            "success": "{}'s comment successfully deleted for such product".format(this_comment.user.get_full_name())
        }
    else:
        res_body = {
            "success": "{}'s comment successfully deleted for such product".format(this_comment.session_id)
        }
    return JsonResponse(res_body, status=204)
