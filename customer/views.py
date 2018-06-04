from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods

from customer.models import User
from .decorators import check_authentication_status


def user_panel(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    if not request.user.is_superuser and request.user != user:
        raise PermissionDenied
    return render(request, 'customer/panel.html', {'user': user})


def user_baskets(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    if not request.user.is_superuser and request.user != user:
        raise PermissionDenied
    return render(request, 'customer/baskets.html', {'user': user})


def user_orders(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    if not request.user.is_superuser and request.user != user:
        raise PermissionDenied
    return render(request, 'customer/orders.html', {'user': user})


def user_favorites(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    if not request.user.is_superuser and request.user != user:
        raise PermissionDenied
    return render(request, 'customer/favorites.html', {'user': user})


def user_settings(request, uuid):
    user = get_object_or_404(User, uuid=uuid)
    if not request.user.is_superuser and request.user != user:
        raise PermissionDenied
    return render(request, 'customer/settings.html', {'user': user})