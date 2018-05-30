from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods

from customer.models import User
from .decorators import check_authentication_status


@check_authentication_status()
def user_panel(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    if request.user != user:
        raise PermissionDenied
    return render(request, 'customer/panel.html', {})


def user_baskets(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    if request.user != user:
        raise PermissionDenied
    return render(request, 'customer/baskets.html', {})


def user_orders(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    if request.user != user:
        raise PermissionDenied
    return render(request, 'customer/orders.html', {})


def user_favorites(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    if request.user != user:
        raise PermissionDenied
    return render(request, 'customer/favorites.html', {})


def user_settings(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    if request.user != user:
        raise PermissionDenied
    return render(request, 'customer/settings.html', {})