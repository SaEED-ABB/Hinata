import logging
from functools import wraps

from django.shortcuts import redirect
from django.http import JsonResponse

logger = logging.getLogger('django.request')


def check_authentication_status():
    """
    Developed by Mohammadreza Sadeghzadeh

    Check user login status, if user doesn't login, can't use api.
    Example:

    @check_authentication_status
    def test(request):
        return
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.user.is_anonymous:
                logger.warning(
                    'Unauthorized',
                    extra={'status_code': 401, 'request': request}
                )
                return JsonResponse({'error': 'Unauthorized'}, status=401)
            return func(request, *args, **kwargs)
        return inner
    return decorator


def check_permission_api(user_type):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.user.is_anonymous:
                return JsonResponse({'error': 'Unauthorized'}, status=401)
            elif not request.user.account_type in user_type:
                return JsonResponse({'error': 'Forbidden Access'}, status=403)
            return func(request, *args, **kwargs)
        return inner
    return decorator


def check_permission_render(user_type, login_url="/"):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.user.is_anonymous or (not request.user.account_type in user_type):
                return redirect(login_url)
            return func(request, *args, **kwargs)
        return inner
    return decorator
