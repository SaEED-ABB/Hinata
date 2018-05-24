from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from customer.models import User
from .decorators import check_permission_render


@require_http_methods(['GET'])
@check_permission_render(['user', 'admin'])
def user_panel(request, slug):
    user = get_object_or_404(User, uuid=slug)
    return render(request, 'customer/panel.html', {})
