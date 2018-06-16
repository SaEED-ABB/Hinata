from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string

from weasyprint import HTML

from customer.models import User, Basket
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


def order_pdf(request, basket_code):

    basket = get_object_or_404(Basket, code=basket_code)

    html_string = render_to_string('customer/order_pdf_template.html', {'basket_info': basket.get_info(), })
    html = HTML(string=html_string)
    pdf_name = 'order_{}.pdf'.format(basket_code)
    html.write_pdf(target='/tmp/{}'.format(pdf_name))
    fs = FileSystemStorage('/tmp')

    with fs.open(pdf_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(pdf_name)
        return response
